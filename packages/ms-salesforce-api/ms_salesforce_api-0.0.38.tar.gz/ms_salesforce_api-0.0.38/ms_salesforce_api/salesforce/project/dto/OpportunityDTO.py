from ms_salesforce_api.salesforce.project.dto.ProjectLineItemDTO import (  # noqa: E501
    ProjectLineItemDTO,
)


class OpportunityDTO(object):
    def __init__(
        self,
        client_fiscal_name,
        client_account_name,
        currency,
        amount,
        invoicing_country_code,
        operation_coordinator_email,
        operation_coordinator_sub_email,
        created_at,
        last_updated_at,
        opportunity_name,
        stage,
        billing_country,
        lead_source,
        project_code,
        project_id,
        project_name,
        project_start_date,
        controller_email,
        controller_sub_email,
        profit_center,
        cost_center,
        project_tier,
        jira_task_url,
        opportunity_percentage,
        billing_lines=[],
        project_line_items=[],
    ):
        self.client_fiscal_name = client_fiscal_name
        self.client_account_name = client_account_name
        self.currency = currency
        self.amount = amount
        self.invoicing_country_code = invoicing_country_code
        self.operation_coordinator_email = operation_coordinator_email
        self.operation_coordinator_sub_email = operation_coordinator_sub_email
        self.created_at = created_at
        self.last_updated_at = last_updated_at
        self.opportunity_name = opportunity_name
        self.stage = stage
        self.billing_country = billing_country
        self.lead_source = lead_source
        self.project_code = project_code
        self.project_id = project_id
        self.project_name = project_name
        self.project_start_date = project_start_date
        self.controller_email = controller_email
        self.controller_sub_email = controller_sub_email
        self.profit_center = profit_center
        self.cost_center = cost_center
        self.project_tier = project_tier
        self.jira_task_url = jira_task_url
        self.opportunity_percentage = opportunity_percentage
        self.billing_lines = billing_lines
        self.project_line_items = project_line_items

    @staticmethod
    def from_salesforce_record(record):
        def _get_client_fiscal_name():
            try:
                return record["Project_Account__r"]["Business_Name__c"]
            except (TypeError, KeyError):
                return ""

        def _get_client_account_name():
            try:
                return record["Project_Account__r"]["Name"]
            except (TypeError, KeyError):
                return ""

        def _get_operation_coordinator_email():
            try:
                return record["Operation_Coordinator__r"]["Name"]
            except (TypeError, KeyError):
                return ""

        def _get_operation_coordinator_sub_email():
            try:
                return record["Operation_Coordinator_Sub__r"]["Name"]
            except (TypeError, KeyError):
                return ""

        def _get_opportunity_name():
            try:
                return record["Opportunity__r"]["Opportunity_Name_Short__c"]
            except (TypeError, KeyError):
                return ""

        def _get_stage():
            try:
                return record["Opportunity__r"]["StageName"]
            except (TypeError, KeyError):
                return ""

        def _get_billing_country():
            try:
                return record["Project_Account__r"]["BillingCountryCode"]
            except (TypeError, KeyError):
                return ""

        def _get_lead_source():
            try:
                return record["Opportunity__r"]["LeadSource"]
            except (TypeError, KeyError):
                return ""

        def _get_controller_email():
            try:
                return record["Operation_Coordinator__r"]["Controller__c"]
            except (TypeError, KeyError):
                return ""

        def _get_controller_sub_email():
            try:
                return record["Operation_Coordinator_Sub__r"][
                    "Controller_SUB__c"
                ]
            except (TypeError, KeyError):
                return ""

        def _get_project_tier():
            try:
                return record["Opportunity__r"]["Tier_Short__c"]
            except (TypeError, KeyError):
                return ""

        def _get_jira_task_url():
            try:
                return record["Opportunity__r"]["JiraComponentURL__c"]
            except (TypeError, KeyError):
                return ""

        def _get_opportunity_percentage():
            try:
                return record["Opportunity__r"]["Probability"]
            except (TypeError, KeyError):
                return ""

        project_line_items = (
            [
                ProjectLineItemDTO.from_salesforce_record(item)
                for item in record.get("Project_Line_Items__r", {}).get(
                    "records", []
                )
            ]
            if record.get("Project_Line_Items__r")
            else []
        )

        return OpportunityDTO(
            client_fiscal_name=_get_client_fiscal_name(),
            client_account_name=_get_client_account_name(),
            currency=record["CurrencyIsoCode"],
            amount=record.get("Total_Project_Amount__c", 0),
            invoicing_country_code=record["Invoicing_Country_Code__c"],
            operation_coordinator_email=_get_operation_coordinator_email(),
            operation_coordinator_sub_email=_get_operation_coordinator_sub_email(),  # noqa: E501
            created_at=record["CreatedDate"],
            last_updated_at=record["LastModifiedDate"],
            opportunity_name=_get_opportunity_name(),
            stage=_get_stage(),
            billing_country=_get_billing_country(),
            lead_source=_get_lead_source(),
            project_code=record["FRM_MSProjectCode__c"],
            project_id=record["Id"],
            project_name=record["Name"],
            project_start_date=record["Start_Date__c"],
            controller_email=_get_controller_email(),
            controller_sub_email=_get_controller_sub_email(),
            profit_center=record["Profit_Center__c"],
            cost_center=record["Cost_Center__c"],
            project_tier=_get_project_tier(),
            jira_task_url=_get_jira_task_url(),
            opportunity_percentage=_get_opportunity_percentage(),
            project_line_items=project_line_items,
        )

    def add_billing_lines(self, billing_lines):
        self.billing_lines.extend(billing_lines)

    def to_dict(self):
        return {
            "client_fiscal_name": self.client_fiscal_name,
            "client_account_name": self.client_account_name,
            "currency": self.currency,
            "amount": self.amount,
            "invoicing_country_code": self.invoicing_country_code,
            "operation_coordinator_email": self.operation_coordinator_email,
            "operation_coordinator_sub_email": self.operation_coordinator_sub_email,  # noqa: E501
            "created_at": self.created_at,
            "last_updated_at": self.last_updated_at,
            "opportunity_name": self.opportunity_name,
            "stage": self.stage,
            "billing_country": self.billing_country,
            "lead_source": self.lead_source,
            "project_code": self.project_code,
            "project_id": self.project_id,
            "project_name": self.project_name,
            "project_start_date": self.project_start_date,
            "controller_email": self.controller_email,
            "controller_sub_email": self.controller_sub_email,
            "profit_center": self.profit_center,
            "cost_center": self.cost_center,
            "project_tier": self.project_tier,
            "jira_task_url": self.jira_task_url,
            "opportunity_percentage": self.opportunity_percentage,
            "billing_lines": [bl.to_dict() for bl in self.billing_lines],
            "project_line_items": [
                pli.to_dict() for pli in self.project_line_items
            ],
        }
