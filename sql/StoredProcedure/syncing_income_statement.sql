DELIMITER //
CREATE PROCEDURE syncing_income_statement()
BEGIN
	insert into fundamentals.income_statement
	(	cik,
		calendarYear,
		period,
		revenue,
		costOfRevenue,
		grossProfit,
		researchAndDevelopmentExpenses,
		generalAndAdministrativeExpenses,
		sellingAndMarketingExpenses,
		sellingGeneralAndAdministrativeExpenses,
		otherExpenses,
		operatingExpenses,
		costAndExpenses,
		interestIncome,
		interestExpense,
		depreciationAndAmortization,
		ebitda,
		operatingIncome,
		totalOtherIncomeExpensesNet,
		incomeBeforeTax,
		incomeTaxExpense,
		netIncome
		)
	select 
	staging.cik,
	staging.calendarYear,
	staging.period,
	staging.revenue,
	staging.costOfRevenue,
	staging.grossProfit,
	staging.researchAndDevelopmentExpenses,
	staging.generalAndAdministrativeExpenses,
	staging.sellingAndMarketingExpenses,
	staging.sellingGeneralAndAdministrativeExpenses,
	staging.otherExpenses,
	staging.operatingExpenses,
	staging.costAndExpenses,
	staging.interestIncome,
	staging.interestExpense,
	staging.depreciationAndAmortization,
	staging.ebitda,
	staging.operatingIncome,
	staging.totalOtherIncomeExpensesNet,
	staging.incomeBeforeTax,
	staging.incomeTaxExpense,
	staging.netIncome
	from fundamentals_staging.incomestatement_staging staging
	left join 
	(
	select ID, cik, calendarYear, period from fundamentals.income_statement
	) formal
	on (staging.cik = formal.cik and staging.calendarYear = formal.calendarYear and staging.period = formal.period)
	where formal.id is null;
END// 
DELIMITER ; # change the delimiter back again.