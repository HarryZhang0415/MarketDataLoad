DELIMITER //
CREATE PROCEDURE syncing_company_info()
BEGIN
	insert into fundamentals.company_info
	(	    
        cik,
        symbol,
        name,
        sicDescription,
        sicGroup,
        sicCode,
        sector,
        subSector,
        exchange,
        headQuarter,
        stateLocation,
        stateOfIncorporation,
        fiscalYearEnd,
        businessAddress,
        mailingAddress,
        taxIdentificationNumber,
        registrantName
		)
	select 
        staging.cik,
        staging.symbol,
        staging.name,
        staging.sicDescription,
        staging.sicGroup,
        staging.sicCode,
        staging.sector,
        staging.subSector,
        staging.exchange,
        staging.headQuarter,
        staging.stateLocation,
        staging.stateOfIncorporation,
        staging.fiscalYearEnd,
        staging.businessAddress,
        staging.mailingAddress,
        staging.taxIdentificationNumber,
        staging.registrantName
	from fundamentals_staging.companyinfo_staging staging
	left join 
	(
	select id, cik from fundamentals.company_info
	) formal
	on (staging.cik = formal.cik)
	where formal.id is null;
END// 
DELIMITER ; # change the delimiter back again.