from openfisca_us.model_api import *


class new_electric_vehicle_credit_eligible(Variable):
    value_type = bool
    entity = TaxUnit
    definition_period = YEAR
    label = "Eligible for new electric vehicle credit"
    documentation = "Eligible for nonrefundable credit for the purchase of a new electric vehicle"
    unit = USD
    reference = "https://www.law.cornell.edu/uscode/text/26/30D"
    defined_for = "purchased_qualifying_new_electric_vehicle"

    def formula(tax_unit, period, parameters):
        ira = parameters(
            period
        ).contrib.congress.senate.democrats.inflation_reduction_act
        # The Inflation Reduction Act introduces income and MSRP limits.
        if not ira.in_effect:
            return True
        p = ira.electric_vehicle_credit.new.eligibility
        agi = tax_unit("adjusted_gross_income", period)
        meets_income_limit = agi <= p.income_limit
        msrp = tax_unit("new_electric_vehicle_msrp", period)
        classification = tax_unit(
            "new_electric_vehicle_classification", period
        )
        meets_msrp_limit = msrp <= p.msrp_limit[classification]
        return meets_income_limit & meets_msrp_limit
