from openfisca_us.model_api import *


class medical_expense_deduction(Variable):
    value_type = float
    entity = TaxUnit
    definition_period = YEAR
    label = "Medical expense deduction"
    reference = "https://www.law.cornell.edu/uscode/text/26/213"
    unit = USD
    documentation = "Medical expenses deducted from taxable income."

    def formula(tax_unit, period, parameters):
        expense = add(tax_unit, period, ["medical_expense"])
        medical = parameters(period).irs.deductions.itemized.medical
        medical_floor = medical.floor * max_(
            tax_unit("adjusted_gross_income", period), 0
        )
        return max_(
            0,
            expense - medical_floor,
        )
