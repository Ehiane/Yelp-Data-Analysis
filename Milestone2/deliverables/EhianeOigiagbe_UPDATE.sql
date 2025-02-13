-- Updating numCheckins:
UPDATE Business
SET numCheckins = (SELECT COALESCE(SUM(C.checkins), 0)
                   FROM Checkin C
                   WHERE C.business_id = Business.business_id);

-- Updating reviewRating:
UPDATE Business
SET reviewRating = (SELECT COALESCE(AVG(R.stars), 0)
                    FROM Review R
                    WHERE R.business_id = Business.business_id);
