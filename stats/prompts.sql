SET @year = 2023;

-- Get the longest, shortest, and total prompts
SELECT
	@shortest_prompt := MIN(LENGTH(word)),
	@longest_prompt := MAX(LENGTH(word)),
	@total_prompts := COUNT(word)
FROM prompts
WHERE
	YEAR(`date`) = @year;

-- Get total prompts with media
SELECT
	@total_media_w_media := COUNT(*) AS `Prompts w/ media`,
	(COUNT(*) / @total_prompts) * 100 AS `Pecent of total`
FROM hosts h
	INNER JOIN host_dates hd
		ON h._id = hd.host_id
	INNER JOIN prompts p
		ON p.host_id = h._id
	INNER JOIN prompt_media pm
		ON pm.prompt_id = p._id
WHERE
	YEAR(hd.date) = @year
	AND YEAR(p.date) = @year;

-- Get total prompts with media but no alt text
SELECT
	COUNT(*) AS `Prompts w/ media w/o alt text`,
	(COUNT(*) / @total_media_w_media) * 100 AS `Pecent of total`
FROM hosts h
	INNER JOIN host_dates hd
		ON h._id = hd.host_id
	INNER JOIN prompts p
		ON p.host_id = h._id
	INNER JOIN prompt_media pm
		ON pm.prompt_id = p._id
WHERE
	YEAR(hd.date) = @year
	AND YEAR(p.date) = @year
	AND pm.alt_text IS NULL;


-- Basic prompt lengths stats
SELECT
	@shortest_prompt AS `Shortest prompt`,
	@longest_prompt AS `Longest prompt`,
	@total_prompts AS `Total prompts this year`,
	AVG(LENGTH(word)) AS `Average prompt length`
FROM prompts
WHERE
	YEAR(`date`) = @year;

-- Get the shortest and longest prompts
SELECT
	h.handle AS `Host`,
	p.date AS `Date`,
	p.word AS `Prompt`,
	LENGTH(p.word) AS `Length`
FROM prompts p
	INNER JOIN hosts h
		ON h._id = p.host_id
WHERE
	YEAR(`date`) = @year
	AND LENGTH(word) IN (@shortest_prompt, @longest_prompt)
ORDER BY
	p.date;

-- Prompts repeated
SELECT
	word AS `Prompt`,
	COUNT(LOWER(word)) AS `Times used`
FROM
	prompts
WHERE
	YEAR(`date`) = @year
GROUP BY
	LOWER(word)
HAVING
	COUNT(LOWER(word)) > 1
ORDER BY
	COUNT(LOWER(word)),
	word;

-- Prompt lengths and times they occurred
SELECT
	LENGTH(word) AS `Length of prompt`,
	COUNT(*) AS `Number of prompts`
FROM
	prompts
WHERE
	YEAR(`date`) = @year
GROUP BY
	LENGTH(LOWER(word))
ORDER BY
	COUNT(*) DESC,
	LENGTH(word) desc;

-- Average length of prompt for each host
SELECT
	h.handle AS `Host`,
	AVG(LENGTH(p.word)) AS `Average length of prompt`
FROM hosts h
	INNER JOIN host_dates hd
		ON h._id = hd.host_id
	INNER JOIN prompts p
		ON p.host_id = h._id
WHERE
	YEAR(hd.date) = @year
	AND YEAR(p.date) = @year
GROUP BY
	h.handle
ORDER BY
	AVG(LENGTH(p.word)) DESC;

-- Get all prompts used for the year
SELECT LOWER(word) AS `Prompt`
FROM prompts
WHERE YEAR(`date`) = @year
ORDER BY `date`;

