CREATE TABLE "task" (
	"id"	INTEGER,
	"title"	TEXT NOT NULL,
	"description"	TEXT,
	"priority"	INTEGER CHECK(priority IN (1, 2, 3)),
	"due_date"	DATETIME,
	"completed"	BOOLEAN,
	"created"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("id")
);