-- Description: Create a view that lists all students that have a score under 80 (strict)
DELIMITER //
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
CREATE PROCEDURE ComputeAverageScoreForUser(
	IN student_id INT
)
BEGIN
	DECLARE avg_score FLOAT;
    SELECT AVG(score) INTO avg_score FROM corrections WHERE user_id = student_id;
	UPDATE users SET average_score = avg_score WHERE id = student_id;
END//
DELIMITER ;