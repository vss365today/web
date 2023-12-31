SET @year = 2023;

-- Get total new subscribers and average per month
SELECT
	COUNT(*) AS `Total`,
	(COUNT(*) / 12) AS `Average`
FROM emails
WHERE
	YEAR(date_added) = @year;

-- Monthly breakdown
SELECT
	MONTHNAME(date_added) AS `Month`,
	COUNT(*) AS `New subscribers`
FROM emails
WHERE
	YEAR(date_added) = @year
GROUP BY
	MONTH(date_added);
