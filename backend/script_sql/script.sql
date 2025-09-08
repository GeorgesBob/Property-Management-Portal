-- Table: public.property

-- DROP TABLE IF EXISTS public.property;

CREATE TABLE IF NOT EXISTS public.property
(
    propertyid integer NOT NULL DEFAULT nextval('property_propertyid_seq'::regclass),
    adress character varying(500) COLLATE pg_catalog."default" NOT NULL,
    propertytype character varying(25) COLLATE pg_catalog."default" NOT NULL,
    status character varying(25) COLLATE pg_catalog."default" NOT NULL,
    purchasedate date NOT NULL,
    price numeric NOT NULL,
    CONSTRAINT property_pkey PRIMARY KEY (propertyid),
    CONSTRAINT property_propertytype_check CHECK (propertytype::text = ANY (ARRAY['Residential'::character varying, 'Commercial'::character varying]::text[])),
    CONSTRAINT property_status_check CHECK (status::text = ANY (ARRAY['Occupied'::character varying, 'Vacant'::character varying]::text[]))
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.property
    OWNER to postgres;


-- Table: public.tenant_management

-- DROP TABLE IF EXISTS public.tenant_management;

CREATE TABLE IF NOT EXISTS public.tenant_management
(
    tenantid integer NOT NULL DEFAULT nextval('tenant_management_tenantid_seq'::regclass),
    name text COLLATE pg_catalog."default",
    contactinfo text COLLATE pg_catalog."default",
    propertyid integer,
    leasetermstart date,
    leasetermend date,
    rentalpaymentstatus text COLLATE pg_catalog."default",
    CONSTRAINT tenant_management_pkey PRIMARY KEY (tenantid),
    CONSTRAINT fk_tenant_property FOREIGN KEY (propertyid)
        REFERENCES public.property (propertyid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT chk_french_phone CHECK (contactinfo ~ '^(?:\+33|0)[1-9](?:\d{2}){4}$'::text),
    CONSTRAINT tenant_management_rentalpaymentstatus_check CHECK (rentalpaymentstatus = ANY (ARRAY['pending'::text, 'in progress'::text, 'completed'::text]))
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tenant_management
    OWNER to postgres;


-- Table: public.maintenance

-- DROP TABLE IF EXISTS public.maintenance;

CREATE TABLE IF NOT EXISTS public.maintenance
(
    taskid integer NOT NULL DEFAULT nextval('maintenance_taskid_seq'::regclass),
    description text COLLATE pg_catalog."default",
    status text COLLATE pg_catalog."default",
    scheduleddate date,
    propertyid integer,
    CONSTRAINT maintenance_pkey PRIMARY KEY (taskid),
    CONSTRAINT fk_maintenance_property FOREIGN KEY (propertyid)
        REFERENCES public.property (propertyid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT maintenance_status_check CHECK (status = ANY (ARRAY['pending'::text, 'in progress'::text, 'completed'::text]))
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.maintenance
    OWNER to postgres;


