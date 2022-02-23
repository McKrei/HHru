CREATE TABLE "vacancies" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(64) NOT NULL,
	"area"	CHAR(16),
	"salary_from"	INTEGER,
	"salary_to"	INTEGER,
	"currency"	CHAR(8),
	"gross"	BOOL,
	"salary"	INTEGER,
	"experience"	VARCHAR(64),
	"schedule"	VARCHAR(64),
	"employment"	VARCHAR(64),
	"professional_roles"	VARCHAR(128),
	PRIMARY KEY("id")
);

CREATE TABLE "description" (
	"vacancy_id"	INTEGER NOT NULL,
	"description"	TEXT,
	FOREIGN KEY("vacancy_id") REFERENCES "vacancies"("id")
);

CREATE TABLE "employers" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE "employer_vacancies" (
	"employer_id"	INTEGER NOT NULL,
	"vacancy_id"	INTEGER NOT NULL,
	FOREIGN KEY("vacancy_id") REFERENCES "vacancies"("id"),
	FOREIGN KEY("employer_id") REFERENCES "employers"("id")
);

CREATE TABLE "key_skills" (
	"vacancy_id"	INTEGER NOT NULL,
	"skill_name"	TEXT NOT NULL,
	FOREIGN KEY("vacancy_id") REFERENCES "vacancies"("id")
);

CREATE TABLE "specializations" (
	"id"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"profarea_id"	TEXT,
	PRIMARY KEY("id"),
	FOREIGN KEY("profarea_id") REFERENCES "specializations"("id")
);

CREATE TABLE "specializations_vacancies" (
	"vacancy_id"	INTEGER NOT NULL,
	"specialization_id"	char(16) NOT NULL,
	FOREIGN KEY("specialization_id") REFERENCES "specializations"("id"),
	FOREIGN KEY("vacancy_id") REFERENCES "vacancies"("id")
);


