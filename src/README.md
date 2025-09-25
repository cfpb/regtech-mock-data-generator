There are five methods of class Correlation, which can be supplied for each variable listed in the yaml spec. Those are: 
    INDEPENDENT: Not used directly in the yaml spec, but is the default class of most data types supplied. 
    DIRECTIVE: Must be indicated when a field's population directly affects the population of the value in another field, such as (in SBL) the `amount_applied_for_flag` field, which when populated with thea value of `1` (applicable and reported), _directs_ the `amount_applied_for` numeric to be populated. In this case, the `amount_applied_for_flag` variable's value _directs_ the population of the `amount_applied_for` variable.
    CASCADING_L1: Must be indicated when a field's value is restricted by the value(s) of another field, which must be indicated in the `dep_field` and `dep_values` fields. For example, in SBL, the value of `ct_loan_term_flag` is restricted by the value of `ct_credit_product`. e.g. the `ct_loan_term_flag` values of `988` (applicable but not provided) and `900` (applicable and reported) are the only values that can be entered when the value of `ct_credit_product` is equal to `1` or `2`, and the `ct_loan_term_flag` value of `999` is the only value that can be entered when the value of `ct_credit_product` is `988` (undetermined or not provided).
    CASCADING_L2: A more complicated version of the above, to be explained later. 
    DEPENDENT: Must be indicated when a field's population relies on the value in another field, such as (in SBL) the `amount_applied_for` numeric field which requires a value of `1` (applicable and reported) in the `amount_applied_for_flag` field. In this case, the population of the `amount_applied_for` is _dependent_ on the `amount_applied_for_flag` variable's value. 


TODO: 

- Account for `NA` and `Exempt` text in HMDA generator fields
--- Maybe generate as numbers and then afterwards impute exempt/NA? 
--- Ignore Exempt / NA possibility altogether and only generate real values?
--- Ignore NA altogether?
- Account for multiple fields enabling `other` free form text fields 
- Extend support for NA and Exempt strings in numeric fields.
- Add flags with dependencies for things like Exempt, non-natural persons, etc. 
- Make the city/state/zip/county/census codes work together with a randomly generated pairing
- Update census resources to include new CT county info