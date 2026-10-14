# AI-Use Disclosure

## 1. Where and How AI Was Used

AI tools (specifically deepseek) were used as a coding assistant and writing aid throughout this project.

**Data Cleaning and Variable Construction:** AI assisted in drafting Stata code to generate key variables and all descriptive statistics, DiD regressions, and the extension were implemented in Python.”.
**Empirical Implementation:** AI provided templates for the Difference-in-Differences regression commands and helped debug error messages in Python.
**Extension Design:** AI was used to brainstorm the price pass-through extension, suggesting the item-specific regressions for soda, fries, and entrées.
**Report Writing:** AI helped polish the English academic writing and translated the core findings between English and Chinese.

## 2. How AI Outputs Were Checked and Verified

All AI-generated content was independently verified.

**Code Validation:** I did not run AI-generated code blindly. I cross-checked the variable definitions against the original paper and the course data dictionary. I ensured that the treatment of closed stores (permanent closures set to 0, temporary closures treated as missing in the baseline) matched the original paper's methodology. The regression outputs were compared directly with the published tables in Card & Krueger (1994).
**Standard Error Correction:** During code validation, I noticed that the AI-generated code used ordinary (homoskedastic) standard errors. Based on my econometrics training, I recognized that DiD regressions should use heteroskedasticity-robust standard errors to ensure accurate inference. I manually modified the Python code to use robust standard errors, which corrected the significance levels and produced more reliable estimates.
**Writing Validation:** All AI-generated text was fact-checked against the original paper. I ensured that the economic interpretations and the magnitude of the coefficients aligned with the actual data results.

## 3. Important AI Errors and Corrections

AI made several errors that I identified and corrected:

**Incorrect Standard Errors:** AI initially provided code using ordinary standard errors. I corrected this by manually implementing heteroskedasticity-robust standard errors, as this is the standard practice for DiD designs with cross-sectional data.
**Runtime Errors:** The AI-generated code contained syntax errors that caused Python to fail. I fed the error messages back to the AI, discussed the underlying issues, and worked iteratively to debug the code until it ran successfully.
**Coefficient Discrepancies:** When my replicated coefficients differed from the original paper, I discussed the differences with the AI. Through this discussion, we identified that the discrepancies were likely due to differences in sample restrictions rather than a fundamental error in the empirical strategy. This helped me justify my results in the final report.
**Formula and Syntax Errors:** AI generated code with formatting errors. I manually corrected the syntax to ensure the equations rendered properly.
**Overgeneralization:** AI initially suggested that the positive price effect definitively proved a specific market model. I corrected this overstatement to reflect that the evidence is consistent with partial pass-through, without claiming definitive proof of the underlying market structure.

## 4. Responsibility Statement

While AI assisted with code generation and writing, I am solely responsible for all data choices, empirical specifications, validation checks, interpretations, and the final conclusions. The AI served as a productivity tool, not a substitute for independent economic reasoning.