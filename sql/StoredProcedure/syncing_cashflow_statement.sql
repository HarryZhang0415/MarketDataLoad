DELIMITER //
CREATE PROCEDURE syncing_cashflow_statement()
BEGIN
	insert into fundamentals.cashflow_statement
	(	
        cik ,
        calendarYear ,
        period ,
        netIncome , 
        depreciationAndAmortization , 
        deferredIncomeTax , 
        stockBasedCompensation , 
        changeInWorkingCapital , 
        accountsReceivables , 
        inventory , 
        accountsPayables , 
        otherWorkingCapital , 
        otherNonCashItems , 
        netCashProvidedByOperatingActivities , 
        investmentsInPropertyPlantAndEquipment , 
        acquisitionsNet , 
        purchasesOfInvestments , 
        salesMaturitiesOfInvestments , 
        otherInvestingActivites , 
        netCashUsedForInvestingActivites , 
        debtRepayment , 
        commonStockIssued , 
        commonStockRepurchased , 
        dividendsPaid , 
        otherFinancingActivites , 
        netCashUsedProvidedByFinancingActivities , 
        effectOfForexChangesOnCash , 
        netChangeInCash , 
        cashAtEndOfPeriod , 
        cashAtBeginningOfPeriod , 
        operatingCashFlow , 
        capitalExpenditure , 
        freeCashFlow
		)
	select 
        staging.cik ,
        staging.calendarYear ,
        staging.period ,
        staging.netIncome , 
        staging.depreciationAndAmortization , 
        staging.deferredIncomeTax , 
        staging.stockBasedCompensation , 
        staging.changeInWorkingCapital , 
        staging.accountsReceivables , 
        staging.inventory , 
        staging.accountsPayables , 
        staging.otherWorkingCapital , 
        staging.otherNonCashItems , 
        staging.netCashProvidedByOperatingActivities , 
        staging.investmentsInPropertyPlantAndEquipment , 
        staging.acquisitionsNet , 
        staging.purchasesOfInvestments , 
        staging.salesMaturitiesOfInvestments , 
        staging.otherInvestingActivites , 
        staging.netCashUsedForInvestingActivites , 
        staging.debtRepayment , 
        staging.commonStockIssued , 
        staging.commonStockRepurchased , 
        staging.dividendsPaid , 
        staging.otherFinancingActivites , 
        staging.netCashUsedProvidedByFinancingActivities , 
        staging.effectOfForexChangesOnCash , 
        staging.netChangeInCash , 
        staging.cashAtEndOfPeriod , 
        staging.cashAtBeginningOfPeriod , 
        staging.operatingCashFlow , 
        staging.capitalExpenditure , 
        staging.freeCashFlow
	from fundamentals_staging.cashflowstatement_staging staging
	left join 
	(
	select ID, cik, calendarYear, period from fundamentals.cashflow_statement
	) formal
	on (staging.cik = formal.cik and staging.calendarYear = formal.calendarYear and staging.period = formal.period)
	where formal.id is null;
END// 
DELIMITER ; # change the delimiter back again.