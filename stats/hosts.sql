SET @year = 2023;

-- Get all hosts
SELECT
	h.handle AS `Host`,
	hd.date AS `Hosting period start date`
FROM hosts h
	INNER JOIN host_dates hd
		ON h._id = hd.host_id
WHERE
	YEAR(hd.date) = @year
ORDER BY
	hd.date;

-- Get repeat hosts
SELECT
	h.handle AS `Host`,
	hd.date AS `Hosting period start date`
FROM
	hosts h
	INNER JOIN host_dates hd
		ON h._id = hd.host_id
WHERE
	YEAR(hd.date) = @year
	AND h._id IN (
		SELECT h._id
		FROM hosts h
		INNER JOIN host_dates hd
			ON h._id = hd.host_id
		WHERE YEAR(hd.date) < @year
)
ORDER BY
	hd.date;

-- Get new hosts
SELECT
	h.handle AS `Host`,
	hd.date AS `Hosting period start date`
FROM
	hosts h
	INNER JOIN host_dates hd
		ON h._id = hd.host_id
WHERE
	YEAR(hd.date) = @year
	AND h._id NOT IN (
		SELECT h._id
		FROM hosts h
		INNER JOIN host_dates hd
			ON h._id = hd.host_id
		WHERE YEAR(hd.date) < @year
)
ORDER BY
	hd.date;
