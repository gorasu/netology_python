/***************************************************************
					Procedure
****************************************************************/
IF EXISTS (SELECT name FROM sysobjects WHERE name = 'GenMapTabSTD1' AND type = 'P')
   DROP PROCEDURE GenMapTabSTD1
GO

CREATE PROCEDURE [dbo].[GenMapTabSTD1] AS
if exists (select * from sysobjects where id = object_id(N'[dbo].[TMP_MTSTD1_ERROR]') and OBJECTPROPERTY(id, N'IsUserTable') = 1)
drop table [dbo].[TMP_MTSTD1_ERROR]
UPDATE DBWPB580..R_FIN_CI SET SYSTEM_NAME = NULL WHERE SYSTEM_NAME = ''
UPDATE DBWPB580..R_FIN_CI SET HOST_FIN_ID = NULL WHERE HOST_FIN_ID = ''
UPDATE DBWPB580..R_FIN_CI SET STDA_SW_RANK = NULL WHERE STDA_SW_RANK = ''
UPDATE DBWPB580..R_FIN_CI SET LRU_TYPE_NAME = NULL WHERE LRU_TYPE_NAME = ''
UPDATE DBWPB580..R_FIN_CI SET LRU_POSITION = NULL WHERE LRU_POSITION = ''
UPDATE DBWPB580..R_FIN_CI SET THW_ID_1 = NULL WHERE THW_ID_1 = ''
UPDATE DBWPB580..R_FIN_CI SET IP_ADDRESS_1 = NULL WHERE IP_ADDRESS_1 = ''
UPDATE DBWPB580..R_FIN_CI SET THW_ID_2 = NULL WHERE THW_ID_2 = ''
UPDATE DBWPB580..R_FIN_CI SET IP_ADDRESS_2 = NULL WHERE IP_ADDRESS_2 = ''
UPDATE DBWPB580..R_FIN_CI SET THW_ID_3 = NULL WHERE THW_ID_3 = ''
UPDATE DBWPB580..R_FIN_CI SET IP_ADDRESS_3 = NULL WHERE IP_ADDRESS_3 = ''
UPDATE DBWPB580..R_FIN_CI SET THW_ID_4 = NULL WHERE THW_ID_4 = ''
UPDATE DBWPB580..R_FIN_CI SET IP_ADDRESS_4 = NULL WHERE IP_ADDRESS_4 = ''
UPDATE DBWPB580..R_FIN_CI SET STDA_DESIGNATION = NULL WHERE STDA_DESIGNATION = ''
--
-- CONTROLS
--
-- FD NULL
--
SELECT
	CAST(FIN AS VARCHAR(50)) AS FIN,
	CAST('FUNCTIONAL_DESIGNATION' AS VARCHAR(8000)) AS ERROR
INTO
	[dbo].[TMP_MTSTD1_ERROR]
FROM
	DBWPB580..R_FIN_CI 
	JOIN DBWPB580..R_ATA ON id_ata = idr_ata
	LEFT JOIN
	(
		SELECT
			MAX(FIN) AS HARD,
			idr_fin_link AS id_soft
		FROM
			DBWPB580..R_FIN_LINK
			JOIN DBWPB580..R_FIN_CI ON id_fin = id_fin_link
		WHERE
			link_type = 'HOST'
		GROUP BY
			idr_fin_link
	) TMP ON id_soft = id_fin
WHERE
	BITEConfReport = 'Yes'
	AND STDA_DESIGNATION IS NULL
	AND FunctionnalDesignation IS NULL
--
-- FD DOUBLE
--
INSERT INTO TMP_MTSTD1_ERROR
(
	FIN,
	ERROR
)
SELECT
	FIN,
	'DOUBLE FUNCTIONAL DESIGNATION'
FROM
	DBWPB580..R_FIN_CI
	JOIN
	(
		SELECT
			FUNCTIONAL_DESIGNATION
		FROM
			(			
				SELECT
					id_fin,
					idr_ata,
					BITEConfReport,
					FIN,
					CASE
						WHEN STDA_DESIGNATION IS NOT NULL THEN STDA_DESIGNATION
						ELSE FunctionnalDesignation
					END FUNCTIONAL_DESIGNATION
				FROM
					DBWPB580..R_FIN_CI
			) FIN_CI			
			JOIN DBWPB580..R_ATA ON id_ata = idr_ata
			LEFT JOIN
			(
				SELECT
					MAX(FIN) AS HARD,
					idr_fin_link AS id_soft
				FROM
					DBWPB580..R_FIN_LINK
					JOIN DBWPB580..R_FIN_CI ON id_fin = id_fin_link
				WHERE
					link_type = 'HOST'
				GROUP BY
					idr_fin_link
			) TMP ON id_soft = id_fin
			LEFT JOIN TMP_MTSTD1_ERROR ON TMP_MTSTD1_ERROR.FIN = FIN_CI.FIN
		WHERE
			BITEConfReport = 'Yes'
			AND TMP_MTSTD1_ERROR.FIN IS NULL
		GROUP BY
			FUNCTIONAL_DESIGNATION
		HAVING COUNT(*) > 1
	) TMP ON FUNCTIONAL_DESIGNATION = CASE WHEN STDA_DESIGNATION IS NOT NULL THEN STDA_DESIGNATION ELSE FunctionnalDesignation END
--
-- LRU TYPE ID & LRU POS DOUBLE
--
INSERT INTO TMP_MTSTD1_ERROR
(
	FIN,
	ERROR
)
SELECT
	FIN,
	'DOUBLE LRU_TYPE_ID LRU_POSITION'
FROM
	DBWPB580..R_FIN_CI
	JOIN
	(
		SELECT
			THW_ID_1,
			LRU_POSITION
		FROM
			DBWPB580..R_FIN_CI			
			JOIN DBWPB580..R_ATA ON id_ata = idr_ata
			LEFT JOIN
			(
				SELECT
					MAX(FIN) AS HARD,
					idr_fin_link AS id_soft
				FROM
					DBWPB580..R_FIN_LINK
					JOIN DBWPB580..R_FIN_CI ON id_fin = id_fin_link
				WHERE
					link_type = 'HOST'
				GROUP BY
					idr_fin_link
			) TMP ON id_soft = id_fin
			LEFT JOIN TMP_MTSTD1_ERROR ON TMP_MTSTD1_ERROR.FIN = DBWPB580..R_FIN_CI.FIN
		WHERE
			BITEConfReport = 'Yes'
			AND TMP_MTSTD1_ERROR.FIN IS NULL
		GROUP BY
			THW_ID_1,
			LRU_POSITION
		HAVING
			COUNT(*) > 1
			AND THW_ID_1 IS NOT NULL
			AND LRU_POSITION IS NOT NULL
	) TMP ON TMP.THW_ID_1 = DBWPB580..R_FIN_CI.THW_ID_1 AND TMP.LRU_POSITION = DBWPB580..R_FIN_CI.LRU_POSITION
--
-- LRU TYPE NAME & LRU POS DOUBLE
--
INSERT INTO TMP_MTSTD1_ERROR
(
	FIN,
	ERROR
)
SELECT
	FIN,
	'DOUBLE LRU_TYPE_NAME LRU_POSITION'
FROM
	DBWPB580..R_FIN_CI
	JOIN
	(
		SELECT
			LRU_TYPE_NAME,
			LRU_POSITION
		FROM
			DBWPB580..R_FIN_CI			
			JOIN DBWPB580..R_ATA ON id_ata = idr_ata
			LEFT JOIN
			(
				SELECT
					MAX(FIN) AS HARD,
					idr_fin_link AS id_soft
				FROM
					DBWPB580..R_FIN_LINK
					JOIN DBWPB580..R_FIN_CI ON id_fin = id_fin_link
				WHERE
					link_type = 'HOST'
				GROUP BY
					idr_fin_link
			) TMP ON id_soft = id_fin
			LEFT JOIN TMP_MTSTD1_ERROR ON TMP_MTSTD1_ERROR.FIN = DBWPB580..R_FIN_CI.FIN
		WHERE
			BITEConfReport = 'Yes'
			AND TMP_MTSTD1_ERROR.FIN IS NULL
		GROUP BY
			LRU_TYPE_NAME,
			LRU_POSITION
		HAVING
			COUNT(*) > 1
			AND LRU_TYPE_NAME IS NOT NULL
			AND LRU_POSITION IS NOT NULL
	) TMP ON TMP.LRU_TYPE_NAME = DBWPB580..R_FIN_CI.LRU_TYPE_NAME AND TMP.LRU_POSITION = DBWPB580..R_FIN_CI.LRU_POSITION
--
-- SW with HARD data
--
INSERT INTO TMP_MTSTD1_ERROR
(
	FIN,
	ERROR
)
SELECT
	DBWPB580..R_FIN_CI.FIN,
	'SW with HARD data'
FROM
	DBWPB580..R_FIN_CI			
	JOIN DBWPB580..R_ATA ON id_ata = idr_ata
	LEFT JOIN
	(
		SELECT
			MAX(FIN) AS HARD,
			idr_fin_link AS id_soft
		FROM
			DBWPB580..R_FIN_LINK
			JOIN DBWPB580..R_FIN_CI ON id_fin = id_fin_link
		WHERE
			link_type = 'HOST'
		GROUP BY
			idr_fin_link
	) TMP ON id_soft = id_fin
	LEFT JOIN TMP_MTSTD1_ERROR ON TMP_MTSTD1_ERROR.FIN = DBWPB580..R_FIN_CI.FIN
WHERE
	BITEConfReport = 'Yes'
	AND TMP_MTSTD1_ERROR.FIN IS NULL
	AND DBWPB580..R_FIN_CI.FIN LIKE '%SW%'
	AND
	(
		IP_ADDRESS_1 IS NOT NULL
		OR LRU_TYPE_NAME IS NOT NULL
		OR THW_ID_1 IS NOT NULL
		OR LRU_POSITION IS NOT NULL
	)
--
-- HARD with SW data
--
INSERT INTO TMP_MTSTD1_ERROR
(
	FIN,
	ERROR
)
SELECT
	DBWPB580..R_FIN_CI.FIN,
	'Bad way HARD/SOFT link in SV'
FROM
	DBWPB580..R_FIN_CI			
	JOIN DBWPB580..R_ATA ON id_ata = idr_ata
	LEFT JOIN
	(
		SELECT
			MAX(FIN) AS HARD,
			idr_fin_link AS id_soft
		FROM
			DBWPB580..R_FIN_LINK
			JOIN DBWPB580..R_FIN_CI ON id_fin = id_fin_link
		WHERE
			link_type = 'HOST'
		GROUP BY
			idr_fin_link
	) TMP ON id_soft = id_fin
	LEFT JOIN TMP_MTSTD1_ERROR ON TMP_MTSTD1_ERROR.FIN = DBWPB580..R_FIN_CI.FIN
WHERE
	BITEConfReport = 'Yes'
	AND TMP_MTSTD1_ERROR.FIN IS NULL
	AND DBWPB580..R_FIN_CI.FIN NOT LIKE '%SW%'
	AND HARD IS NOT NULL
--
-- Unexisting HOST FIN ID
--
INSERT INTO TMP_MTSTD1_ERROR
(
	FIN,
	ERROR
)
SELECT
	DBWPB580..R_FIN_CI.FIN,
	'Unexisting HOST FIN ID'
FROM
	DBWPB580..R_FIN_CI			
	JOIN DBWPB580..R_ATA ON id_ata = idr_ata
	LEFT JOIN
	(
		SELECT
			MAX(FIN) AS HARD,
			idr_fin_link AS id_soft
		FROM
			DBWPB580..R_FIN_LINK
			JOIN DBWPB580..R_FIN_CI ON id_fin = id_fin_link
		WHERE
			link_type = 'HOST'
		GROUP BY
			idr_fin_link
	) TMP ON id_soft = id_fin
	LEFT JOIN TMP_MTSTD1_ERROR ON TMP_MTSTD1_ERROR.FIN = DBWPB580..R_FIN_CI.FIN
	LEFT JOIN
	(
		SELECT
			DBWPB580..R_FIN_CI.FIN
		FROM
			DBWPB580..R_FIN_CI			
			JOIN DBWPB580..R_ATA ON id_ata = idr_ata
			LEFT JOIN
			(
				SELECT
					MAX(FIN) AS HARD,
					idr_fin_link AS id_soft
				FROM
					DBWPB580..R_FIN_LINK
					JOIN DBWPB580..R_FIN_CI ON id_fin = id_fin_link
				WHERE
					link_type = 'HOST'
				GROUP BY
					idr_fin_link
			) TMP ON id_soft = id_fin
			LEFT JOIN TMP_MTSTD1_ERROR ON TMP_MTSTD1_ERROR.FIN = DBWPB580..R_FIN_CI.FIN
		WHERE
			BITEConfReport = 'Yes'
			AND TMP_MTSTD1_ERROR.FIN IS NULL
	) HOST ON HOST.FIN = HARD
WHERE
	BITEConfReport = 'Yes'
	AND TMP_MTSTD1_ERROR.FIN IS NULL
	AND DBWPB580..R_FIN_CI.FIN LIKE '%SW%'
	AND HOST.FIN IS NULL
--
-- Generate MT
--
SELECT
	*,
	';'
FROM
	(
		SELECT
			LEFT(DBWPB580..R_FIN_CI.FIN, 20) AS FIN,
			CASE
				WHEN DBWPB580..R_FIN_CI.FIN LIKE '%SW%' THEN 'S'
				ELSE 'H'
			END FIN_TYPE,
			CASE
				WHEN STDA_DESIGNATION IS NOT NULL THEN
					STDA_DESIGNATION
				ELSE FunctionnalDesignation
			END FUNCTIONAL_DESIGNATION,
			LEFT(STDA_SW_RANK, 2) AS STDA_SW_RANK,
			ATACODE,
			CASE
				WHEN IP_ADDRESS_1 IS NOT NULL AND LRU_TYPE_NAME IS NOT NULL AND THW_ID_1 IS NOT NULL AND LRU_POSITION IS NOT NULL
					AND NOT
					(
						IP_ADDRESS_2 IS NOT NULL
						AND THW_ID_2 IS NOT NULL
						AND
						(
							IP_ADDRESS_2 <> IP_ADDRESS_1
							OR THW_ID_2 <> THW_ID_1
						)
					)
				THEN dbo.FormatIP(IP_ADDRESS_1)
				ELSE NULL
			END IP_ADDRESS,
			CASE
				WHEN IP_ADDRESS_1 IS NOT NULL AND LRU_TYPE_NAME IS NOT NULL AND THW_ID_1 IS NOT NULL AND LRU_POSITION IS NOT NULL THEN LEFT(LRU_TYPE_NAME, 15)
				ELSE NULL
			END LRU_TYPE_NAME,
			CASE
				WHEN IP_ADDRESS_1 IS NOT NULL AND LRU_TYPE_NAME IS NOT NULL AND THW_ID_1 IS NOT NULL AND LRU_POSITION IS NOT NULL
					AND NOT
					(
						IP_ADDRESS_2 IS NOT NULL
						AND THW_ID_2 IS NOT NULL
						AND
						(
							IP_ADDRESS_2 <> IP_ADDRESS_1
							OR THW_ID_2 <> THW_ID_1
						)
					)
				THEN LEFT(THW_ID_1, 15)
				ELSE NULL
			END LRU_TYPE_ID,
			CASE
				WHEN IP_ADDRESS_1 IS NOT NULL AND LRU_TYPE_NAME IS NOT NULL AND THW_ID_1 IS NOT NULL AND LRU_POSITION IS NOT NULL THEN LEFT(LRU_POSITION, 10)
				ELSE NULL
			END LRU_POSITION,
			LEFT(SYSTEM_NAME, 25) AS SYSTEM_NAME,
			LEFT(HARD, 20) AS [HOST_FIN_ID],
			CASE
				WHEN DBWPB580..R_FIN_CI.FIN LIKE '%SW%' THEN
					CASE
						WHEN FunctionnalDesignation LIKE '%SPP%' AND FunctionnalDesignation LIKE '%SCI%' THEN 1
						ELSE 0
					END
				ELSE NULL
			END SPP
		FROM
			DBWPB580..R_FIN_CI 
			JOIN DBWPB580..R_ATA ON id_ata = idr_ata
			LEFT JOIN
			(
				SELECT
					MAX(FIN) AS HARD,
					idr_fin_link AS id_soft
				FROM
					DBWPB580..R_FIN_LINK
					JOIN DBWPB580..R_FIN_CI ON id_fin = id_fin_link
				WHERE
					link_type = 'HOST'
				GROUP BY
					idr_fin_link
			) TMP ON id_soft = id_fin
			LEFT JOIN TMP_MTSTD1_ERROR ON TMP_MTSTD1_ERROR.FIN = DBWPB580..R_FIN_CI.FIN
		WHERE
			BITEConfReport = 'Yes'
			AND TMP_MTSTD1_ERROR.FIN IS NULL
		
		UNION
		
		SELECT
			DBWPB580..R_FIN_CI.FIN + '_A' AS FIN,
			CASE
				WHEN DBWPB580..R_FIN_CI.FIN LIKE '%SW%' THEN 'S'
				ELSE 'H'
			END FIN_TYPE,
			CASE
				WHEN STDA_DESIGNATION IS NOT NULL THEN
					CASE
						WHEN DBWPB580..R_FIN_CI.FIN LIKE '%SW%' THEN LEFT(STDA_DESIGNATION, 13)
						ELSE LEFT(STDA_DESIGNATION, 19)
					END
				ELSE FunctionnalDesignation
			END + '_A' FUNCTIONAL_DESIGNATION,
			STDA_SW_RANK,
			ATACODE,
			dbo.FormatIP(IP_ADDRESS_1),
			LEFT(LRU_TYPE_NAME, 13) + '_A',
			THW_ID_1 AS LRU_TYPE_ID,
			LRU_POSITION,
			SYSTEM_NAME,
			DBWPB580..R_FIN_CI.FIN AS [HOST_FIN_ID],
			CASE
				WHEN DBWPB580..R_FIN_CI.FIN LIKE '%SW%' THEN
					CASE
						WHEN FunctionnalDesignation LIKE '%SPP%' AND FunctionnalDesignation LIKE '%SCI%' THEN 1
						ELSE 0
					END
				ELSE NULL
			END SPP
		FROM
			DBWPB580..R_FIN_CI 
			JOIN DBWPB580..R_ATA ON id_ata = idr_ata
			LEFT JOIN
			(
				SELECT
					MAX(FIN) AS HARD,
					idr_fin_link AS id_soft
				FROM
					DBWPB580..R_FIN_LINK
					JOIN DBWPB580..R_FIN_CI ON id_fin = id_fin_link
				WHERE
					link_type = 'HOST'
				GROUP BY
					idr_fin_link
			) TMP ON id_soft = id_fin
			LEFT JOIN TMP_MTSTD1_ERROR ON TMP_MTSTD1_ERROR.FIN = DBWPB580..R_FIN_CI.FIN
		WHERE
			BITEConfReport = 'Yes'
			AND TMP_MTSTD1_ERROR.FIN IS NULL
			AND IP_ADDRESS_2 IS NOT NULL
			AND THW_ID_2 IS NOT NULL
			AND
			(
				IP_ADDRESS_2 <> IP_ADDRESS_1
				OR THW_ID_2 <> THW_ID_1
			)
		
		UNION
		
		SELECT
			DBWPB580..R_FIN_CI.FIN + '_B' AS FIN,
			CASE
				WHEN DBWPB580..R_FIN_CI.FIN LIKE '%SW%' THEN 'S'
				ELSE 'H'
			END FIN_TYPE,
			CASE
				WHEN STDA_DESIGNATION IS NOT NULL THEN
					CASE
						WHEN DBWPB580..R_FIN_CI.FIN LIKE '%SW%' THEN LEFT(STDA_DESIGNATION, 13)
						ELSE LEFT(STDA_DESIGNATION, 19)
					END
				ELSE FunctionnalDesignation
			END + '_B' FUNCTIONAL_DESIGNATION,
			STDA_SW_RANK,
			ATACODE,
			dbo.FormatIP(IP_ADDRESS_2),
			LEFT(LRU_TYPE_NAME, 13) + '_B',
			THW_ID_2 AS LRU_TYPE_ID,
			LRU_POSITION,
			SYSTEM_NAME,
			DBWPB580..R_FIN_CI.FIN AS [HOST_FIN_ID],
			CASE
				WHEN DBWPB580..R_FIN_CI.FIN LIKE '%SW%' THEN
					CASE
						WHEN FunctionnalDesignation LIKE '%SPP%' AND FunctionnalDesignation LIKE '%SCI%' THEN 1
						ELSE 0
					END
				ELSE NULL
			END SPP
		FROM
			DBWPB580..R_FIN_CI 
			JOIN DBWPB580..R_ATA ON id_ata = idr_ata
			LEFT JOIN
			(
				SELECT
					MAX(FIN) AS HARD,
					idr_fin_link AS id_soft
				FROM
					DBWPB580..R_FIN_LINK
					JOIN DBWPB580..R_FIN_CI ON id_fin = id_fin_link
				WHERE
					link_type = 'HOST'
				GROUP BY
					idr_fin_link
			) TMP ON id_soft = id_fin
			LEFT JOIN TMP_MTSTD1_ERROR ON TMP_MTSTD1_ERROR.FIN = DBWPB580..R_FIN_CI.FIN
		WHERE
			BITEConfReport = 'Yes'
			AND TMP_MTSTD1_ERROR.FIN IS NULL
			AND IP_ADDRESS_2 IS NOT NULL
			AND THW_ID_2 IS NOT NULL
			AND
			(
				IP_ADDRESS_2 <> IP_ADDRESS_1
				OR THW_ID_2 <> THW_ID_1
			)
		
		UNION
		
		SELECT
			DBWPB580..R_FIN_CI.FIN + '_C' AS FIN,
			CASE
				WHEN DBWPB580..R_FIN_CI.FIN LIKE '%SW%' THEN 'S'
				ELSE 'H'
			END FIN_TYPE,
			CASE
				WHEN STDA_DESIGNATION IS NOT NULL THEN
					CASE
						WHEN DBWPB580..R_FIN_CI.FIN LIKE '%SW%' THEN LEFT(STDA_DESIGNATION, 13)
						ELSE LEFT(STDA_DESIGNATION, 19)
					END
				ELSE FunctionnalDesignation
			END + '_C' FUNCTIONAL_DESIGNATION,
			STDA_SW_RANK,
			ATACODE,
			dbo.FormatIP(IP_ADDRESS_3),
			LEFT(LRU_TYPE_NAME, 13) + '_C',
			THW_ID_3 AS LRU_TYPE_ID,
			LRU_POSITION,
			SYSTEM_NAME,
			DBWPB580..R_FIN_CI.FIN AS [HOST_FIN_ID],
			CASE
				WHEN DBWPB580..R_FIN_CI.FIN LIKE '%SW%' THEN
					CASE
						WHEN FunctionnalDesignation LIKE '%SPP%' AND FunctionnalDesignation LIKE '%SCI%' THEN 1
						ELSE 0
					END
				ELSE NULL
			END SPP
		FROM
			DBWPB580..R_FIN_CI 
			JOIN DBWPB580..R_ATA ON id_ata = idr_ata
			LEFT JOIN
			(
				SELECT
					MAX(FIN) AS HARD,
					idr_fin_link AS id_soft
				FROM
					DBWPB580..R_FIN_LINK
					JOIN DBWPB580..R_FIN_CI ON id_fin = id_fin_link
				WHERE
					link_type = 'HOST'
				GROUP BY
					idr_fin_link
			) TMP ON id_soft = id_fin
			LEFT JOIN TMP_MTSTD1_ERROR ON TMP_MTSTD1_ERROR.FIN = DBWPB580..R_FIN_CI.FIN
		WHERE
			BITEConfReport = 'Yes'
			AND TMP_MTSTD1_ERROR.FIN IS NULL
			AND IP_ADDRESS_2 IS NOT NULL
			AND THW_ID_2 IS NOT NULL
			AND IP_ADDRESS_3 IS NOT NULL
			AND THW_ID_3 IS NOT NULL
		
		UNION
		
		SELECT
			DBWPB580..R_FIN_CI.FIN + '_D' AS FIN,
			CASE
				WHEN DBWPB580..R_FIN_CI.FIN LIKE '%SW%' THEN 'S'
				ELSE 'H'
			END FIN_TYPE,
			CASE
				WHEN STDA_DESIGNATION IS NOT NULL THEN
					CASE
						WHEN DBWPB580..R_FIN_CI.FIN LIKE '%SW%' THEN LEFT(STDA_DESIGNATION, 13)
						ELSE LEFT(STDA_DESIGNATION, 19)
					END
				ELSE FunctionnalDesignation
			END + '_D' FUNCTIONAL_DESIGNATION,
			STDA_SW_RANK,
			ATACODE,
			dbo.FormatIP(IP_ADDRESS_4),
			LEFT(LRU_TYPE_NAME, 13) + '_D',
			THW_ID_4 AS LRU_TYPE_ID,
			LRU_POSITION,
			SYSTEM_NAME,
			DBWPB580..R_FIN_CI.FIN AS [HOST_FIN_ID],
			CASE
				WHEN DBWPB580..R_FIN_CI.FIN LIKE '%SW%' THEN
					CASE
						WHEN FunctionnalDesignation LIKE '%SPP%' AND FunctionnalDesignation LIKE '%SCI%' THEN 1
						ELSE 0
					END
				ELSE NULL
			END SPP
		FROM
			DBWPB580..R_FIN_CI 
			JOIN DBWPB580..R_ATA ON id_ata = idr_ata
			LEFT JOIN
			(
				SELECT
					MAX(FIN) AS HARD,
					idr_fin_link AS id_soft
				FROM
					DBWPB580..R_FIN_LINK
					JOIN DBWPB580..R_FIN_CI ON id_fin = id_fin_link
				WHERE
					link_type = 'HOST'
				GROUP BY
					idr_fin_link
			) TMP ON id_soft = id_fin
			LEFT JOIN TMP_MTSTD1_ERROR ON TMP_MTSTD1_ERROR.FIN = DBWPB580..R_FIN_CI.FIN
		WHERE
			BITEConfReport = 'Yes'
			AND TMP_MTSTD1_ERROR.FIN IS NULL
			AND IP_ADDRESS_2 IS NOT NULL
			AND THW_ID_2 IS NOT NULL
			AND IP_ADDRESS_3 IS NOT NULL
			AND THW_ID_3 IS NOT NULL
			AND IP_ADDRESS_4 IS NOT NULL
			AND THW_ID_4 IS NOT NULL
	) TMP
ORDER BY
	FIN_TYPE,
	CASE WHEN ISNUMERIC(LRU_POSITION) = 1 THEN CONVERT(INTEGER, LRU_POSITION) ELSE 0 END,
	FIN

/***************************************************************
					Group report
****************************************************************/
if not exists(SELECT * FROM T_REPORT_GROUP WHERE report_group_label='Others')
begin
	INSERT INTO
		T_REPORT_GROUP (
			report_group_label
		)
	VALUES (
		'Others'
	)
end

/***************************************************************
					Line in T_DBActions
****************************************************************/

DELETE FROM T_DBActions WHERE label='Generate Mapping Table Standard 1 Data File'

INSERT INTO 
	T_dbactions (
		label,
		command,
		comments,
		template_page,
		parameters,
		report_commentary,
		mandatory_fields,
		report_group_idr
	) 
SELECT 
	'Generate Mapping Table Standard 1 Data File',
	'EXECUTE [GenMapTabSTD1]',
	'- Export Mapping Table data file Standard 1',
	NULL,
	NULL,
	NULL,
	NULL,
	report_group_id 
FROM 
	T_REPORT_GROUP 
WHERE 
	report_group_label='Others'
