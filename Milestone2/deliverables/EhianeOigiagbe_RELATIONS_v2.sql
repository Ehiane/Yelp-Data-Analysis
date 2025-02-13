CREATE TABLE Business (
    business_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(255) NOT NULL,
    state VARCHAR(50) NOT NULL,
    postal_code VARCHAR(10),
    latitude FLOAT,
    longitude FLOAT,
    stars FLOAT,
    review_count INT,
    is_open INT,
    numCheckins INT DEFAULT 0,
    reviewRating FLOAT DEFAULT 0.0
);

CREATE TABLE Users (
    user_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    yelping_since DATE,
    review_count INT DEFAULT 0,
    fans INT,
    average_stars FLOAT,
    funny INT,
    useful INT,
    cool INT
);

CREATE TABLE Review (
    review_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    business_id VARCHAR(255) NOT NULL,
    stars INT CHECK(stars >= 1 AND stars <= 5),
    date DATE NOT NULL,
    text TEXT,
    useful INT,
    funny INT,
    cool INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

CREATE TABLE Checkin (
    business_id VARCHAR(255) NOT NULL,
    day VARCHAR(50) NOT NULL,
    hour VARCHAR(50) NOT NULL,
    checkins INT DEFAULT 0,
    PRIMARY KEY (business_id, day, hour),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);
