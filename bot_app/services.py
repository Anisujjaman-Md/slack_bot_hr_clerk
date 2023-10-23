from datetime import datetime, timedelta
import calendar
from django.db.models import Count
from slack.errors import SlackApiError
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from config import settings
from leave_management.models import LeaveApplication, LeavePolicy, RestrictedDays, LeaveType

slack_signing_secret = settings.SLACK_SIGNING_SECRET
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/api/v1/slack-bot")
client = WebClient(token=settings.SLACK_TOKEN)


class LeaveApplicationService:
    def __init__(self):
        pass

    def check_how_many_leave_taken(self, user_id, channel_id, leave_type):
        report_year = datetime.now().year
        report_month = datetime.now().month

        report_for_year = LeaveApplication.objects.filter(
            leave_status=LeaveApplication.APPROVE,
            start_date__year=report_year,
            employee_id=user_id,
            Leave_type__leave_type_name=leave_type,
        )
        report_for_month = LeaveApplication.objects.filter(
            leave_status=LeaveApplication.APPROVE,
            start_date__month=report_month,
            employee_id=user_id,
            Leave_type__leave_type_name=leave_type,
        )
        leave_type_query_set = LeaveType.objects.get(leave_type_name=leave_type)
        max_leaves_per_year = leave_type_query_set.days_allowed_in_a_year
        max_leaves_per_month = leave_type_query_set.days_allowed_in_a_month

        if len(report_for_year) >= max_leaves_per_year:
            client.chat_postMessage(channel=channel_id,
                                    text=f"Warning! Your maximum {leave_type} leave is already taken for this year "
                                         f":cry:")
        else:
            if len(report_for_month) >= max_leaves_per_month:
                client.chat_postMessage(channel=channel_id,
                                        text=f"Warning! Your maximum {leave_type} leave is already taken for this month "
                                             f":cry:")
        return True

    def leave_form(self, channel_id):
        current_date = datetime.now().strftime("%Y-%m-%d")
        leave_types = LeaveType.objects.all()
        leave_type_block = {
            "type": "section",
            "block_id": "sectionBlockWithStaticSelect",
            "text": {
                "type": "mrkdwn",
                "text": "Pick the type of leave you need:"
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select an item",
                    "emoji": True
                },
                "action_id": "leave_type_block_action"
            }
        }
        options = [
            {
                "text": {
                    "type": "plain_text",
                    "text": leave_type.leave_type_name.capitalize(),
                    "emoji": True
                },
                "value": leave_type.leave_type_name
            }
            for leave_type in leave_types
        ]

        leave_type_block["accessory"]["options"] = options

        start_date_block = {
            "type": "section",
            "block_id": "sectionBlockWithStartDate",
            "text": {
                "type": "mrkdwn",
                "text": "Pick a start date:"
            },
            "accessory": {
                "type": "datepicker",
                "initial_date": current_date,
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a date",
                    "emoji": True
                },
                "action_id": "start_date_action"
            }
        }

        end_date_block = {
            "type": "section",
            "block_id": "sectionBlockWithEndDate",
            "text": {
                "type": "mrkdwn",
                "text": "Pick an end date:"
            },
            "accessory": {
                "type": "datepicker",
                "initial_date": current_date,
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a date",
                    "emoji": True
                },
                "action_id": "end_date_action"
            }
        }

        comment_block = {
            "type": "input",
            "block_id": "sectionBlockWithComment",
            "element": {
                "type": "plain_text_input",
                "action_id": "comment_input",
                "multiline": True,
                "placeholder": {
                    "type": "plain_text",
                    "text": "Type your comment here"
                }
            },
            "label": {
                "type": "plain_text",
                "text": "Comment"
            }
        }

        send_button_block = {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Submit",
                        "emoji": True
                    },
                    "action_id": "submit_form_action"
                }
            ]
        }
        blocks = [leave_type_block, start_date_block, end_date_block, comment_block, send_button_block]

        response = client.chat_postMessage(channel=channel_id, blocks=blocks)

        return response

    def check_date_in_restricted_days(self, start_date_str, end_date_str, channel_id):
        today = datetime.now().date()
        restricted_dates = RestrictedDays.objects.filter(date__gte=today).values_list('date', flat=True)

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        date_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        for date in date_list:
            if date in restricted_dates:
                client.chat_postMessage(channel=channel_id, text="Sorry! You cannot take this date is *restricted* for "
                                                                 "leave :cry:")
                return True

        return False


class LeaveReportService:
    def __init__(self):
        pass

    def leave_report(self, event, channel_id):
        user_id = event.get("user")
        text = event.get("text")
        parts = text.split()

        # Check if the input format is valid
        if len(parts) == 3 and parts[0].lower() == "report":
            report_month = int(parts[1])
            report_year = int(parts[2])

            report = LeaveApplication.objects.filter(
                leave_status=LeaveApplication.APPROVE,
                start_date__month=report_month,
                start_date__year=report_year,
                employee_id=user_id
            ).values(
                'start_date',
                'employee_id'
            ).annotate(
                total=Count('start_date')
            )

            blocks = []
            for entry in report:
                month = entry['start_date']
                # Create a dynamic text block with values from the current entry
                block = {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Date: {month}"
                    }
                }
                blocks.append(block)

            month = calendar.month_name[report_month]
            blocks.insert(0, {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f" Hey: <@{user_id}>, Report For: *{month} {report_year}* & Total Approved Leave : {len(report)}"
                }
            })

            # Create a list of blocks and send the message to a Slack channel
            client.chat_postMessage(
                channel=channel_id,
                blocks=blocks
            )
        else:
            message = "Invalid input format. Expected format: *'Report MM YYYY'*"
            try:
                client.chat_postMessage(channel=channel_id, text=message)
                response = {"message_sent": True}
            except SlackApiError as e:
                response = {"error": e.response["error"]}
        return {"message_sent": True}
