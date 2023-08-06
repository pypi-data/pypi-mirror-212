from urllib.parse import quote

from gc_google_services_api.bigquery import BigQueryManager


class BigQueryExporter:
    def __init__(self, project_id, dataset_id):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = BigQueryManager(
            project_id=project_id, dataset_id=dataset_id
        )
        self.batch_size = 200
        self.schemas = {
            "last_executed_at": {
                "last_executed_at": "TIMESTAMP",
            },
            "opportunities": {
                "client_fiscal_name": "STRING",
                "client_account_name": "STRING",
                "currency": "STRING",
                "amount": "FLOAT",
                "invoicing_country_code": "STRING",
                "operation_coordinator_email": "STRING",
                "operation_coordinator_sub_email": "STRING",
                "created_at": "TIMESTAMP",
                "last_updated_at": "TIMESTAMP",
                "opportunity_name": "STRING",
                "stage": "STRING",
                "billing_country": "STRING",
                "lead_source": "STRING",
                "project_code": "STRING",
                "project_id": "STRING",
                "project_name": "STRING",
                "project_start_date": "DATE",
                "controller_email": "STRING",
                "controller_sub_email": "STRING",
                "profit_center": "STRING",
                "cost_center": "STRING",
                "project_tier": "STRING",
                "jira_task_url": "STRING",
                "opportunity_percentage": "STRING",
            },
            "billing_lines": {
                "id": "STRING",
                "project_id": "STRING",
                "name": "STRING",
                "currency": "STRING",
                "created_date": "TIMESTAMP",
                "last_modified_date": "TIMESTAMP",
                "billing_amount": "FLOAT",
                "billing_date": "DATE",
                "billing_period_ending_date": "DATE",
                "billing_period_starting_date": "DATE",
                "hourly_price": "FLOAT",
                "revenue_dedication": "FLOAT",
                "billing_plan_amount": "STRING",
                "billing_plan_billing_date": "DATE",
                "billing_plan_item": "STRING",
                "billing_plan_service_end_date": "DATE",
                "billing_plan_service_start_date": "DATE",
            },
            "project_line_items": {
                "country": "STRING",
                "project_id": "STRING",
                "created_date": "TIMESTAMP",
                "effort": "STRING",
                "ending_date": "DATE",
                "id": "STRING",
                "last_modified_date": "TIMESTAMP",
                "ms_pli_name": "STRING",
                "product_name": "STRING",
                "quantity": "FLOAT",
                "starting_date": "DATE",
                "total_price": "STRING",
                "unit_price": "STRING",
            },
        }

        for table_name, table_schema in self.schemas.items():
            self.client.create_table_if_not_exists(table_name, table_schema)

    def _export_opportunities(self, opportunities):
        opportunities_values = []
        for opp in opportunities:
            project_start_date = (
                f'DATE "{opp["project_start_date"]}"'
                if opp["project_start_date"]
                else "NULL"
            )
            profit_center = (
                f'"{opp["profit_center"]}"' if opp["profit_center"] else "NULL"
            )
            cost_center = (
                f'"{opp["cost_center"]}"' if opp["cost_center"] else "NULL"
            )

            opportunities_values.append(
                f"""
                (
                    "{opp['client_fiscal_name']}",
                    "{opp['client_account_name']}",
                    "{opp['currency']}",
                    {opp['amount']},
                    "{opp['invoicing_country_code']}",
                    "{opp['operation_coordinator_email']}",
                    "{opp['operation_coordinator_sub_email']}",
                    TIMESTAMP "{opp['created_at']}",
                    TIMESTAMP "{opp['last_updated_at']}",
                    "{opp['opportunity_name']}",
                    "{opp['stage']}",
                    "{opp['billing_country']}",
                    "{opp['lead_source']}",
                    "{opp['project_code']}",
                    "{opp['project_id']}",
                    "{opp['project_name']}",
                    {project_start_date},
                    "{opp['controller_email']}",
                    "{opp['controller_sub_email']}",
                    {profit_center},
                    {cost_center},
                    "{opp['project_tier']}",
                    "{quote(opp['jira_task_url'], safe='s')}",
                   "{opp['opportunity_percentage']}"
                )
                """
            )
        if opportunities_values:
            insert_opportunities_query = f"""
                INSERT INTO `{self.dataset_id}.{self.project_id}.opportunities` (
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
                    opportunity_percentage
                ) VALUES {', '.join(opportunities_values)};
            """
            self.client.execute_query(insert_opportunities_query, None)

    def _export_billing_lines(self, opportunities):
        billing_lines_values = []
        for opp in opportunities:
            for bl in opp["billing_lines"]:
                billing_date = (
                    f'DATE "{bl["billing_date"]}"'
                    if bl["billing_date"]
                    else "NULL"
                )
                billing_period_ending_date = (
                    f'DATE "{bl["billing_period_ending_date"]}"'
                    if bl["billing_period_ending_date"]
                    else "NULL"
                )
                billing_period_starting_date = (
                    f'DATE "{bl["billing_period_starting_date"]}"'
                    if bl["billing_period_starting_date"]
                    else "NULL"
                )
                billing_plan_billing_date = (
                    f'DATE "{bl["billing_plan_billing_date"]}"'
                    if bl["billing_plan_billing_date"]
                    else "NULL"
                )
                billing_plan_service_end_date = (
                    f'DATE "{bl["billing_plan_service_end_date"]}"'
                    if bl["billing_plan_service_end_date"]
                    else "NULL"
                )
                billing_plan_service_start_date = (
                    f'DATE "{bl["billing_plan_service_start_date"]}"'
                    if bl["billing_plan_service_start_date"]
                    else "NULL"
                )

                billing_lines_values.append(
                    f"""
                    (
                        "{bl['id']}",
                        "{bl['project_id']}",
                        "{bl['name']}",
                        "{bl['currency']}",
                        TIMESTAMP "{bl['created_date']}",
                        TIMESTAMP "{bl['last_modified_date']}",
                        {bl['billing_amount']},
                        {billing_date},
                        {billing_period_ending_date},
                        {billing_period_starting_date},
                        {bl['hourly_price'] if bl['hourly_price'] else 'NULL'},
                        {bl['revenue_dedication'] if bl['revenue_dedication'] else 'NULL'},
                        "{bl['billing_plan_amount']}",
                        {billing_plan_billing_date},
                        "{bl['billing_plan_item']}",
                        {billing_plan_service_end_date},
                        {billing_plan_service_start_date}
                    )
                    """
                )
        if billing_lines_values:
            insert_billing_lines_query = f"""
                INSERT INTO `{self.dataset_id}.{self.project_id}.billing_lines` (
                    id,
                    project_id,
                    name,
                    currency,
                    created_date,
                    last_modified_date,
                    billing_amount,
                    billing_date,
                    billing_period_ending_date,
                    billing_period_starting_date,
                    hourly_price,
                    revenue_dedication,
                    billing_plan_amount,
                    billing_plan_billing_date,
                    billing_plan_item,
                    billing_plan_service_end_date,
                    billing_plan_service_start_date
                ) VALUES {', '.join(billing_lines_values)};
            """

            self.client.execute_query(insert_billing_lines_query, None)

    def _export_PLIs(self, opportunities):
        project_line_items_values = []
        for opp in opportunities:
            project_id = opp["project_id"]
            for pli in opp["project_line_items"]:
                effort = f"{pli['effort']}" if pli["effort"] else "NULL"
                total_price = (
                    f"{pli['total_price']}" if pli["total_price"] else "NULL"
                )
                unit_price = (
                    f"{pli['unit_price']}" if pli["unit_price"] else "NULL"
                )
                ending_date = (
                    f'DATE "{pli["ending_date"]}"'
                    if pli["ending_date"]
                    else "NULL"
                )
                starting_date = (
                    f'DATE "{pli["starting_date"]}"'
                    if pli["starting_date"]
                    else "NULL"
                )

                project_line_items_values.append(
                    f"""
                    (
                        "{pli['country']}",
                        TIMESTAMP "{pli['created_date']}",
                        "{effort}",
                        {ending_date},
                        "{pli['id']}",
                        TIMESTAMP "{pli['last_modified_date']}",
                        "{pli['ms_pli_name']}",
                        "{pli['product_name']}",
                        {pli['quantity'] if pli['quantity'] else 0.0},
                        {starting_date},
                        "{total_price}",
                        "{unit_price}",
                        "{project_id}"
                    )
                    """
                )

        if project_line_items_values:
            insert_project_line_items_query = f"""
                INSERT INTO `{self.dataset_id}.{self.project_id}.project_line_items` (
                    country,
                    created_date,
                    effort,
                    ending_date,
                    id,
                    last_modified_date,
                    ms_pli_name,
                    product_name,
                    quantity,
                    starting_date,
                    total_price,
                    unit_price,
                    project_id
                ) VALUES {', '.join(project_line_items_values)};
            """
            self.client.execute_query(insert_project_line_items_query, None)

    def export_data(self, opportunities):
        opportunities_batches = [
            opportunities[i : i + self.batch_size]  # noqa: E203
            for i in range(0, len(opportunities), self.batch_size)
        ]
        for batch in opportunities_batches:
            self._export_opportunities(batch)

            self._export_billing_lines(batch)

            self._export_PLIs(batch)
