cd "C:\Users\桑榆非晚\Desktop\NJ_minimum_wage_replication"

import delimited "data/raw/public.csv", clear

gen fte1 = empft + nmgrs + 0.5 * emppt
label var fte1 "FTE employment in Wave 1"

gen fte2 = empft2 + nmgrs2 + 0.5 * emppt2
label var fte2 "FTE employment in Wave 2"

gen perm_closed = (status2 == 3)
gen temp_closed = inlist(status2, 2, 4, 5)

replace fte2 = 0 if perm_closed == 1

replace fte2 = . if temp_closed == 1

gen delta_fte = fte2 - fte1
label var delta_fte "Change in FTE employment (Wave 2 - Wave 1)"

gen pct_change = delta_fte / fte1
label var pct_change "Percentage change in FTE employment"

gen nj = (state == 1)
label var nj "New Jersey dummy"

gen gap = 0
replace gap = (5.05 - wage_st) / wage_st if nj == 1 & wage_st < 5.05
label var gap "Proportional wage increase needed to reach new minimum wage"

sum fte1 fte2 delta_fte nj gap pct_change

capture mkdir data/processed

export delimited "data/processed/cleaned_data.csv", replace