-- public.results определение

-- Drop table

-- DROP TABLE public.results;

CREATE TABLE public.results (
	id bigserial NOT NULL,
	speech varchar NULL,
	is_depression bool NULL,
	CONSTRAINT results_pk PRIMARY KEY (id)
);