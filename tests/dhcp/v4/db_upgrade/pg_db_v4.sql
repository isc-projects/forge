--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.17
-- Dumped by pg_dump version 9.6.17

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: lease4dumpdata(); Type: FUNCTION; Schema: public; Owner: !db_user!
--

CREATE FUNCTION public.lease4dumpdata() RETURNS TABLE(address inet, hwaddr text, client_id text, valid_lifetime bigint, expire timestamp with time zone, subnet_id bigint, fqdn_fwd integer, fqdn_rev integer, hostname text, state text, user_context text)
    LANGUAGE sql
    AS $$
    SELECT ('0.0.0.0'::inet + l.address),
            encode(l.hwaddr,'hex'),
            encode(l.client_id,'hex'),
            l.valid_lifetime,
            l.expire,
            l.subnet_id,
            l.fqdn_fwd::int,
            l.fqdn_rev::int,
            l.hostname,
            s.name,
            l.user_context
    FROM lease4 l
         left outer join lease_state s on (l.state = s.state)
    ORDER BY l.address;
$$;


ALTER FUNCTION public.lease4dumpdata() OWNER TO !db_user!;

--
-- Name: lease4dumpheader(); Type: FUNCTION; Schema: public; Owner: !db_user!
--

CREATE FUNCTION public.lease4dumpheader() RETURNS text
    LANGUAGE sql
    AS $$
    select cast('address,hwaddr,client_id,valid_lifetime,expire,subnet_id,fqdn_fwd,fqdn_rev,hostname,state,user_context' as text) as result;
$$;


ALTER FUNCTION public.lease4dumpheader() OWNER TO !db_user!;

--
-- Name: lease6dumpdata(); Type: FUNCTION; Schema: public; Owner: !db_user!
--

CREATE FUNCTION public.lease6dumpdata() RETURNS TABLE(address text, duid text, valid_lifetime bigint, expire timestamp with time zone, subnet_id bigint, pref_lifetime bigint, name text, iaid integer, prefix_len smallint, fqdn_fwd integer, fqdn_rev integer, hostname text, state text, hwaddr text, hwtype smallint, hwaddr_source text, user_context text)
    LANGUAGE sql
    AS $$
    SELECT (l.address,
            encode(l.duid,'hex'),
            l.valid_lifetime,
            l.expire,
            l.subnet_id,
            l.pref_lifetime,
            t.name,
            l.iaid,
            l.prefix_len,
            l.fqdn_fwd::int,
            l.fqdn_rev::int,
            l.hostname,
            s.name,
            encode(l.hwaddr,'hex'),
            l.hwtype,
            h.name,
            l.user_context

     )
     FROM lease6 l
         left outer join lease6_types t on (l.lease_type = t.lease_type)
         left outer join lease_state s on (l.state = s.state)
         left outer join lease_hwaddr_source h on (l.hwaddr_source = h.hwaddr_source)
     ORDER BY l.address;
$$;


ALTER FUNCTION public.lease6dumpdata() OWNER TO !db_user!;

--
-- Name: lease6dumpheader(); Type: FUNCTION; Schema: public; Owner: !db_user!
--

CREATE FUNCTION public.lease6dumpheader() RETURNS text
    LANGUAGE sql
    AS $$
    select cast('address,duid,valid_lifetime,expire,subnet_id,pref_lifetime,lease_type,iaid,prefix_len,fqdn_fwd,fqdn_rev,hostname,state,hwaddr,hwtype,hwaddr_source,user_context' as text) as result;
$$;


ALTER FUNCTION public.lease6dumpheader() OWNER TO !db_user!;

--
-- Name: proc_stat_lease4_delete(); Type: FUNCTION; Schema: public; Owner: !db_user!
--

CREATE FUNCTION public.proc_stat_lease4_delete() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF OLD.state < 2 THEN
        -- Decrement the state count if record exists
        UPDATE lease4_stat SET leases = leases - 1
        WHERE subnet_id = OLD.subnet_id AND OLD.state = state;
    END IF;

    -- Return is ignored since this is an after insert
    RETURN NULL;
END;
$$;


ALTER FUNCTION public.proc_stat_lease4_delete() OWNER TO !db_user!;

--
-- Name: proc_stat_lease4_insert(); Type: FUNCTION; Schema: public; Owner: !db_user!
--

CREATE FUNCTION public.proc_stat_lease4_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.state < 2 THEN
        UPDATE lease4_stat
            SET leases = leases + 1
            WHERE subnet_id = NEW.subnet_id AND state = NEW.state;

        IF NOT FOUND THEN
            INSERT INTO lease4_stat VALUES (new.subnet_id, new.state, 1);
        END IF;
    END IF;

    -- Return is ignored since this is an after insert
    RETURN NULL;
END;
$$;


ALTER FUNCTION public.proc_stat_lease4_insert() OWNER TO !db_user!;

--
-- Name: proc_stat_lease4_update(); Type: FUNCTION; Schema: public; Owner: !db_user!
--

CREATE FUNCTION public.proc_stat_lease4_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF OLD.state != NEW.state THEN
        IF OLD.state < 2 THEN
            -- Decrement the old state count if record exists
            UPDATE lease4_stat SET leases = leases - 1
            WHERE subnet_id = OLD.subnet_id AND state = OLD.state;
        END IF;

        IF NEW.state < 2 THEN
            -- Increment the new state count if record exists
            UPDATE lease4_stat SET leases = leases + 1
            WHERE subnet_id = NEW.subnet_id AND state = NEW.state;

            -- Insert new state record if it does not exist
            IF NOT FOUND THEN
                INSERT INTO lease4_stat VALUES (NEW.subnet_id, NEW.state, 1);
            END IF;
        END IF;
    END IF;

    -- Return is ignored since this is an after insert
    RETURN NULL;
END;
$$;


ALTER FUNCTION public.proc_stat_lease4_update() OWNER TO !db_user!;

--
-- Name: proc_stat_lease6_delete(); Type: FUNCTION; Schema: public; Owner: !db_user!
--

CREATE FUNCTION public.proc_stat_lease6_delete() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF OLD.state < 2 THEN
        -- Decrement the state count if record exists
        UPDATE lease6_stat SET leases = leases - 1
        WHERE subnet_id = OLD.subnet_id AND lease_type = OLD.lease_type
        AND OLD.state = state;
    END IF;

    -- Return is ignored since this is an after insert
    RETURN NULL;
END;
$$;


ALTER FUNCTION public.proc_stat_lease6_delete() OWNER TO !db_user!;

--
-- Name: proc_stat_lease6_insert(); Type: FUNCTION; Schema: public; Owner: !db_user!
--

CREATE FUNCTION public.proc_stat_lease6_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.state < 2 THEN
        UPDATE lease6_stat
        SET leases = leases + 1
        WHERE
        subnet_id = NEW.subnet_id AND lease_type = NEW.lease_type
        AND state = NEW.state;

        IF NOT FOUND THEN
            INSERT INTO lease6_stat
            VALUES (NEW.subnet_id, NEW.lease_type, NEW.state, 1);
        END IF;
    END IF;

    -- Return is ignored since this is an after insert
    RETURN NULL;
END;
$$;


ALTER FUNCTION public.proc_stat_lease6_insert() OWNER TO !db_user!;

--
-- Name: proc_stat_lease6_update(); Type: FUNCTION; Schema: public; Owner: !db_user!
--

CREATE FUNCTION public.proc_stat_lease6_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF OLD.state != NEW.state THEN
        IF OLD.state < 2 THEN
            -- Decrement the old state count if record exists
            UPDATE lease6_stat SET leases = leases - 1
            WHERE subnet_id = OLD.subnet_id AND lease_type = OLD.lease_type
            AND state = OLD.state;
        END IF;

        IF NEW.state < 2 THEN
            -- Increment the new state count if record exists
            UPDATE lease6_stat SET leases = leases + 1
            WHERE subnet_id = NEW.subnet_id AND lease_type = NEW.lease_type
            AND state = NEW.state;

            -- Insert new state record if it does not exist
            IF NOT FOUND THEN
                INSERT INTO lease6_stat VALUES (NEW.subnet_id, NEW.lease_type, NEW.state, 1);
            END IF;
        END IF;
    END IF;

    -- Return is ignored since this is an after insert
    RETURN NULL;
END;
$$;


ALTER FUNCTION public.proc_stat_lease6_update() OWNER TO !db_user!;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: dhcp4_options; Type: TABLE; Schema: public; Owner: !db_user!
--

CREATE TABLE public.dhcp4_options (
    option_id integer NOT NULL,
    code smallint NOT NULL,
    value bytea,
    formatted_value text,
    space character varying(128) DEFAULT NULL::character varying,
    persistent boolean DEFAULT false NOT NULL,
    dhcp_client_class character varying(128) DEFAULT NULL::character varying,
    dhcp4_subnet_id bigint,
    host_id integer,
    scope_id smallint NOT NULL,
    user_context text
);


ALTER TABLE public.dhcp4_options OWNER TO !db_user!;

--
-- Name: dhcp4_options_option_id_seq; Type: SEQUENCE; Schema: public; Owner: !db_user!
--

CREATE SEQUENCE public.dhcp4_options_option_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dhcp4_options_option_id_seq OWNER TO !db_user!;

--
-- Name: dhcp4_options_option_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: !db_user!
--

ALTER SEQUENCE public.dhcp4_options_option_id_seq OWNED BY public.dhcp4_options.option_id;


--
-- Name: dhcp6_options; Type: TABLE; Schema: public; Owner: !db_user!
--

CREATE TABLE public.dhcp6_options (
    option_id integer NOT NULL,
    code integer NOT NULL,
    value bytea,
    formatted_value text,
    space character varying(128) DEFAULT NULL::character varying,
    persistent boolean DEFAULT false NOT NULL,
    dhcp_client_class character varying(128) DEFAULT NULL::character varying,
    dhcp6_subnet_id bigint,
    host_id integer,
    scope_id smallint NOT NULL,
    user_context text
);


ALTER TABLE public.dhcp6_options OWNER TO !db_user!;

--
-- Name: dhcp6_options_option_id_seq; Type: SEQUENCE; Schema: public; Owner: !db_user!
--

CREATE SEQUENCE public.dhcp6_options_option_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dhcp6_options_option_id_seq OWNER TO !db_user!;

--
-- Name: dhcp6_options_option_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: !db_user!
--

ALTER SEQUENCE public.dhcp6_options_option_id_seq OWNED BY public.dhcp6_options.option_id;


--
-- Name: dhcp_option_scope; Type: TABLE; Schema: public; Owner: !db_user!
--

CREATE TABLE public.dhcp_option_scope (
    scope_id smallint NOT NULL,
    scope_name character varying(32) DEFAULT NULL::character varying
);


ALTER TABLE public.dhcp_option_scope OWNER TO !db_user!;

--
-- Name: host_identifier_type; Type: TABLE; Schema: public; Owner: !db_user!
--

CREATE TABLE public.host_identifier_type (
    type smallint NOT NULL,
    name character varying(32) DEFAULT NULL::character varying
);


ALTER TABLE public.host_identifier_type OWNER TO !db_user!;

--
-- Name: hosts; Type: TABLE; Schema: public; Owner: !db_user!
--

CREATE TABLE public.hosts (
    host_id integer NOT NULL,
    dhcp_identifier bytea NOT NULL,
    dhcp_identifier_type smallint NOT NULL,
    dhcp4_subnet_id bigint,
    dhcp6_subnet_id bigint,
    ipv4_address bigint,
    hostname character varying(255) DEFAULT NULL::character varying,
    dhcp4_client_classes character varying(255) DEFAULT NULL::character varying,
    dhcp6_client_classes character varying(255) DEFAULT NULL::character varying,
    dhcp4_next_server bigint,
    dhcp4_server_hostname character varying(64) DEFAULT NULL::character varying,
    dhcp4_boot_file_name character varying(128) DEFAULT NULL::character varying,
    user_context text,
    auth_key character varying(32) DEFAULT NULL::character varying
);


ALTER TABLE public.hosts OWNER TO !db_user!;

--
-- Name: hosts_host_id_seq; Type: SEQUENCE; Schema: public; Owner: !db_user!
--

CREATE SEQUENCE public.hosts_host_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hosts_host_id_seq OWNER TO !db_user!;

--
-- Name: hosts_host_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: !db_user!
--

ALTER SEQUENCE public.hosts_host_id_seq OWNED BY public.hosts.host_id;


--
-- Name: ipv6_reservations; Type: TABLE; Schema: public; Owner: !db_user!
--

CREATE TABLE public.ipv6_reservations (
    reservation_id integer NOT NULL,
    address character varying(39) NOT NULL,
    prefix_len smallint DEFAULT '128'::smallint NOT NULL,
    type smallint DEFAULT '0'::smallint NOT NULL,
    dhcp6_iaid integer,
    host_id integer NOT NULL
);


ALTER TABLE public.ipv6_reservations OWNER TO !db_user!;

--
-- Name: ipv6_reservations_reservation_id_seq; Type: SEQUENCE; Schema: public; Owner: !db_user!
--

CREATE SEQUENCE public.ipv6_reservations_reservation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ipv6_reservations_reservation_id_seq OWNER TO !db_user!;

--
-- Name: ipv6_reservations_reservation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: !db_user!
--

ALTER SEQUENCE public.ipv6_reservations_reservation_id_seq OWNED BY public.ipv6_reservations.reservation_id;


--
-- Name: lease4; Type: TABLE; Schema: public; Owner: !db_user!
--

CREATE TABLE public.lease4 (
    address bigint NOT NULL,
    hwaddr bytea,
    client_id bytea,
    valid_lifetime bigint,
    expire timestamp with time zone,
    subnet_id bigint,
    fqdn_fwd boolean,
    fqdn_rev boolean,
    hostname character varying(255),
    state bigint DEFAULT 0,
    user_context text
);


ALTER TABLE public.lease4 OWNER TO !db_user!;

--
-- Name: lease4_stat; Type: TABLE; Schema: public; Owner: !db_user!
--

CREATE TABLE public.lease4_stat (
    subnet_id bigint NOT NULL,
    state bigint NOT NULL,
    leases bigint
);


ALTER TABLE public.lease4_stat OWNER TO !db_user!;

--
-- Name: lease6; Type: TABLE; Schema: public; Owner: !db_user!
--

CREATE TABLE public.lease6 (
    address character varying(39) NOT NULL,
    duid bytea,
    valid_lifetime bigint,
    expire timestamp with time zone,
    subnet_id bigint,
    pref_lifetime bigint,
    lease_type smallint,
    iaid integer,
    prefix_len smallint,
    fqdn_fwd boolean,
    fqdn_rev boolean,
    hostname character varying(255),
    state bigint DEFAULT 0,
    hwaddr bytea,
    hwtype smallint,
    hwaddr_source smallint,
    user_context text
);


ALTER TABLE public.lease6 OWNER TO !db_user!;

--
-- Name: lease6_stat; Type: TABLE; Schema: public; Owner: !db_user!
--

CREATE TABLE public.lease6_stat (
    subnet_id bigint NOT NULL,
    lease_type smallint NOT NULL,
    state bigint NOT NULL,
    leases bigint
);


ALTER TABLE public.lease6_stat OWNER TO !db_user!;

--
-- Name: lease6_types; Type: TABLE; Schema: public; Owner: !db_user!
--

CREATE TABLE public.lease6_types (
    lease_type smallint NOT NULL,
    name character varying(5)
);


ALTER TABLE public.lease6_types OWNER TO !db_user!;

--
-- Name: lease_hwaddr_source; Type: TABLE; Schema: public; Owner: !db_user!
--

CREATE TABLE public.lease_hwaddr_source (
    hwaddr_source integer NOT NULL,
    name character varying(40) DEFAULT NULL::character varying
);


ALTER TABLE public.lease_hwaddr_source OWNER TO !db_user!;

--
-- Name: lease_state; Type: TABLE; Schema: public; Owner: !db_user!
--

CREATE TABLE public.lease_state (
    state bigint NOT NULL,
    name character varying(64) NOT NULL
);


ALTER TABLE public.lease_state OWNER TO !db_user!;

--
-- Name: logs; Type: TABLE; Schema: public; Owner: !db_user!
--

CREATE TABLE public.logs (
    "timestamp" timestamp with time zone DEFAULT now(),
    address character varying(43),
    log text NOT NULL
);


ALTER TABLE public.logs OWNER TO !db_user!;

--
-- Name: schema_version; Type: TABLE; Schema: public; Owner: !db_user!
--

CREATE TABLE public.schema_version (
    version integer NOT NULL,
    minor integer
);


ALTER TABLE public.schema_version OWNER TO !db_user!;

--
-- Name: dhcp4_options option_id; Type: DEFAULT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.dhcp4_options ALTER COLUMN option_id SET DEFAULT nextval('public.dhcp4_options_option_id_seq'::regclass);


--
-- Name: dhcp6_options option_id; Type: DEFAULT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.dhcp6_options ALTER COLUMN option_id SET DEFAULT nextval('public.dhcp6_options_option_id_seq'::regclass);


--
-- Name: hosts host_id; Type: DEFAULT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.hosts ALTER COLUMN host_id SET DEFAULT nextval('public.hosts_host_id_seq'::regclass);


--
-- Name: ipv6_reservations reservation_id; Type: DEFAULT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.ipv6_reservations ALTER COLUMN reservation_id SET DEFAULT nextval('public.ipv6_reservations_reservation_id_seq'::regclass);


--
-- Data for Name: dhcp4_options; Type: TABLE DATA; Schema: public; Owner: !db_user!
--

COPY public.dhcp4_options (option_id, code, value, formatted_value, space, persistent, dhcp_client_class, dhcp4_subnet_id, host_id, scope_id, user_context) FROM stdin;
1	6	\N	10.1.1.202,10.1.1.203	dhcp4	f	\N	\N	1	3	\N
\.


--
-- Name: dhcp4_options_option_id_seq; Type: SEQUENCE SET; Schema: public; Owner: !db_user!
--

SELECT pg_catalog.setval('public.dhcp4_options_option_id_seq', 1, true);


--
-- Data for Name: dhcp6_options; Type: TABLE DATA; Schema: public; Owner: !db_user!
--

COPY public.dhcp6_options (option_id, code, value, formatted_value, space, persistent, dhcp_client_class, dhcp6_subnet_id, host_id, scope_id, user_context) FROM stdin;
\.


--
-- Name: dhcp6_options_option_id_seq; Type: SEQUENCE SET; Schema: public; Owner: !db_user!
--

SELECT pg_catalog.setval('public.dhcp6_options_option_id_seq', 1, false);


--
-- Data for Name: dhcp_option_scope; Type: TABLE DATA; Schema: public; Owner: !db_user!
--

COPY public.dhcp_option_scope (scope_id, scope_name) FROM stdin;
0	global
1	subnet
2	client-class
3	host
\.


--
-- Data for Name: host_identifier_type; Type: TABLE DATA; Schema: public; Owner: !db_user!
--

COPY public.host_identifier_type (type, name) FROM stdin;
0	hw-address
1	duid
2	circuit-id
3	client-id
4	flex-id
\.


--
-- Data for Name: hosts; Type: TABLE DATA; Schema: public; Owner: !db_user!
--

COPY public.hosts (host_id, dhcp_identifier, dhcp_identifier_type, dhcp4_subnet_id, dhcp6_subnet_id, ipv4_address, hostname, dhcp4_client_classes, dhcp6_client_classes, dhcp4_next_server, dhcp4_server_hostname, dhcp4_boot_file_name, user_context, auth_key) FROM stdin;
1	\\x010a0b0c0d0e0f	0	1	\N	3232248525		special_snowflake,office		3221225985	hal9000	/dev/null	\N	\N
\.


--
-- Name: hosts_host_id_seq; Type: SEQUENCE SET; Schema: public; Owner: !db_user!
--

SELECT pg_catalog.setval('public.hosts_host_id_seq', 1, true);


--
-- Data for Name: ipv6_reservations; Type: TABLE DATA; Schema: public; Owner: !db_user!
--

COPY public.ipv6_reservations (reservation_id, address, prefix_len, type, dhcp6_iaid, host_id) FROM stdin;
\.


--
-- Name: ipv6_reservations_reservation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: !db_user!
--

SELECT pg_catalog.setval('public.ipv6_reservations_reservation_id_seq', 1, false);


--
-- Data for Name: lease4; Type: TABLE DATA; Schema: public; Owner: !db_user!
--

COPY public.lease4 (address, hwaddr, client_id, valid_lifetime, expire, subnet_id, fqdn_fwd, fqdn_rev, hostname, state, user_context) FROM stdin;
3232248330	\\xff010203ff04	\\x	4000	2021-02-17 11:42:51-08	1	f	f		0	
\.


--
-- Data for Name: lease4_stat; Type: TABLE DATA; Schema: public; Owner: !db_user!
--

COPY public.lease4_stat (subnet_id, state, leases) FROM stdin;
1	0	1
\.


--
-- Data for Name: lease6; Type: TABLE DATA; Schema: public; Owner: !db_user!
--

COPY public.lease6 (address, duid, valid_lifetime, expire, subnet_id, pref_lifetime, lease_type, iaid, prefix_len, fqdn_fwd, fqdn_rev, hostname, state, hwaddr, hwtype, hwaddr_source, user_context) FROM stdin;
\.


--
-- Data for Name: lease6_stat; Type: TABLE DATA; Schema: public; Owner: !db_user!
--

COPY public.lease6_stat (subnet_id, lease_type, state, leases) FROM stdin;
\.


--
-- Data for Name: lease6_types; Type: TABLE DATA; Schema: public; Owner: !db_user!
--

COPY public.lease6_types (lease_type, name) FROM stdin;
0	IA_NA
1	IA_TA
2	IA_PD
\.


--
-- Data for Name: lease_hwaddr_source; Type: TABLE DATA; Schema: public; Owner: !db_user!
--

COPY public.lease_hwaddr_source (hwaddr_source, name) FROM stdin;
0	HWADDR_SOURCE_UNKNOWN
1	HWADDR_SOURCE_RAW
2	HWADDR_SOURCE_IPV6_LINK_LOCAL
4	HWADDR_SOURCE_DUID
8	HWADDR_SOURCE_CLIENT_ADDR_RELAY_OPTION
16	HWADDR_SOURCE_REMOTE_ID
32	HWADDR_SOURCE_SUBSCRIBER_ID
64	HWADDR_SOURCE_DOCSIS_CMTS
128	HWADDR_SOURCE_DOCSIS_MODEM
\.


--
-- Data for Name: lease_state; Type: TABLE DATA; Schema: public; Owner: !db_user!
--

COPY public.lease_state (state, name) FROM stdin;
0	default
1	declined
2	expired-reclaimed
\.


--
-- Data for Name: logs; Type: TABLE DATA; Schema: public; Owner: !db_user!
--

COPY public.logs ("timestamp", address, log) FROM stdin;
\.


--
-- Data for Name: schema_version; Type: TABLE DATA; Schema: public; Owner: !db_user!
--

COPY public.schema_version (version, minor) FROM stdin;
5	1
\.


--
-- Name: dhcp4_options dhcp4_options_pkey; Type: CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.dhcp4_options
    ADD CONSTRAINT dhcp4_options_pkey PRIMARY KEY (option_id);


--
-- Name: dhcp6_options dhcp6_options_pkey; Type: CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.dhcp6_options
    ADD CONSTRAINT dhcp6_options_pkey PRIMARY KEY (option_id);


--
-- Name: dhcp_option_scope dhcp_option_scope_pkey; Type: CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.dhcp_option_scope
    ADD CONSTRAINT dhcp_option_scope_pkey PRIMARY KEY (scope_id);


--
-- Name: host_identifier_type host_identifier_type_pkey; Type: CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.host_identifier_type
    ADD CONSTRAINT host_identifier_type_pkey PRIMARY KEY (type);


--
-- Name: hosts hosts_pkey; Type: CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.hosts
    ADD CONSTRAINT hosts_pkey PRIMARY KEY (host_id);


--
-- Name: ipv6_reservations ipv6_reservations_pkey; Type: CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.ipv6_reservations
    ADD CONSTRAINT ipv6_reservations_pkey PRIMARY KEY (reservation_id);


--
-- Name: ipv6_reservations key_dhcp6_address_prefix_len; Type: CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.ipv6_reservations
    ADD CONSTRAINT key_dhcp6_address_prefix_len UNIQUE (address, prefix_len);


--
-- Name: lease4 lease4_pkey; Type: CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.lease4
    ADD CONSTRAINT lease4_pkey PRIMARY KEY (address);


--
-- Name: lease4_stat lease4_stat_pkey; Type: CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.lease4_stat
    ADD CONSTRAINT lease4_stat_pkey PRIMARY KEY (subnet_id, state);


--
-- Name: lease6 lease6_pkey; Type: CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.lease6
    ADD CONSTRAINT lease6_pkey PRIMARY KEY (address);


--
-- Name: lease6_stat lease6_stat_pkey; Type: CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.lease6_stat
    ADD CONSTRAINT lease6_stat_pkey PRIMARY KEY (subnet_id, lease_type, state);


--
-- Name: lease6_types lease6_types_pkey; Type: CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.lease6_types
    ADD CONSTRAINT lease6_types_pkey PRIMARY KEY (lease_type);


--
-- Name: lease_hwaddr_source lease_hwaddr_source_pkey; Type: CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.lease_hwaddr_source
    ADD CONSTRAINT lease_hwaddr_source_pkey PRIMARY KEY (hwaddr_source);


--
-- Name: lease_state lease_state_pkey; Type: CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.lease_state
    ADD CONSTRAINT lease_state_pkey PRIMARY KEY (state);


--
-- Name: schema_version schema_version_pkey; Type: CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.schema_version
    ADD CONSTRAINT schema_version_pkey PRIMARY KEY (version);


--
-- Name: address_id; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE INDEX address_id ON public.logs USING btree (address);


--
-- Name: fk_dhcp4_options_host1_idx; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE INDEX fk_dhcp4_options_host1_idx ON public.dhcp4_options USING btree (host_id);


--
-- Name: fk_dhcp4_options_scope_idx; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE INDEX fk_dhcp4_options_scope_idx ON public.dhcp4_options USING btree (scope_id);


--
-- Name: fk_dhcp6_options_host1_idx; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE INDEX fk_dhcp6_options_host1_idx ON public.dhcp6_options USING btree (host_id);


--
-- Name: fk_dhcp6_options_scope_idx; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE INDEX fk_dhcp6_options_scope_idx ON public.dhcp6_options USING btree (scope_id);


--
-- Name: fk_host_identifier_type; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE INDEX fk_host_identifier_type ON public.hosts USING btree (dhcp_identifier_type);


--
-- Name: fk_ipv6_reservations_host_idx; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE INDEX fk_ipv6_reservations_host_idx ON public.ipv6_reservations USING btree (host_id);


--
-- Name: key_dhcp4_identifier_subnet_id; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE UNIQUE INDEX key_dhcp4_identifier_subnet_id ON public.hosts USING btree (dhcp_identifier, dhcp_identifier_type, dhcp4_subnet_id) WHERE ((dhcp4_subnet_id IS NOT NULL) AND (dhcp4_subnet_id <> 0));


--
-- Name: key_dhcp4_ipv4_address_subnet_id; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE UNIQUE INDEX key_dhcp4_ipv4_address_subnet_id ON public.hosts USING btree (ipv4_address, dhcp4_subnet_id) WHERE ((ipv4_address IS NOT NULL) AND (ipv4_address <> 0));


--
-- Name: key_dhcp6_identifier_subnet_id; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE UNIQUE INDEX key_dhcp6_identifier_subnet_id ON public.hosts USING btree (dhcp_identifier, dhcp_identifier_type, dhcp6_subnet_id) WHERE ((dhcp6_subnet_id IS NOT NULL) AND (dhcp6_subnet_id <> 0));


--
-- Name: lease4_by_client_id_subnet_id; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE INDEX lease4_by_client_id_subnet_id ON public.lease4 USING btree (client_id, subnet_id);


--
-- Name: lease4_by_hwaddr_subnet_id; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE INDEX lease4_by_hwaddr_subnet_id ON public.lease4 USING btree (hwaddr, subnet_id);


--
-- Name: lease4_by_state_expire; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE INDEX lease4_by_state_expire ON public.lease4 USING btree (state, expire);


--
-- Name: lease4_by_subnet_id; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE INDEX lease4_by_subnet_id ON public.lease4 USING btree (subnet_id);


--
-- Name: lease6_by_duid_iaid_subnet_id; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE INDEX lease6_by_duid_iaid_subnet_id ON public.lease6 USING btree (duid, iaid, subnet_id);


--
-- Name: lease6_by_state_expire; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE INDEX lease6_by_state_expire ON public.lease6 USING btree (state, expire);


--
-- Name: lease6_by_subnet_id_lease_type; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE INDEX lease6_by_subnet_id_lease_type ON public.lease6 USING btree (subnet_id, lease_type);


--
-- Name: timestamp_id; Type: INDEX; Schema: public; Owner: !db_user!
--

CREATE INDEX timestamp_id ON public.logs USING btree ("timestamp");


--
-- Name: lease4 stat_lease4_delete; Type: TRIGGER; Schema: public; Owner: !db_user!
--

CREATE TRIGGER stat_lease4_delete AFTER DELETE ON public.lease4 FOR EACH ROW EXECUTE PROCEDURE public.proc_stat_lease4_delete();


--
-- Name: lease4 stat_lease4_insert; Type: TRIGGER; Schema: public; Owner: !db_user!
--

CREATE TRIGGER stat_lease4_insert AFTER INSERT ON public.lease4 FOR EACH ROW EXECUTE PROCEDURE public.proc_stat_lease4_insert();


--
-- Name: lease4 stat_lease4_update; Type: TRIGGER; Schema: public; Owner: !db_user!
--

CREATE TRIGGER stat_lease4_update AFTER UPDATE ON public.lease4 FOR EACH ROW EXECUTE PROCEDURE public.proc_stat_lease4_update();


--
-- Name: lease6 stat_lease6_delete; Type: TRIGGER; Schema: public; Owner: !db_user!
--

CREATE TRIGGER stat_lease6_delete AFTER DELETE ON public.lease6 FOR EACH ROW EXECUTE PROCEDURE public.proc_stat_lease6_delete();


--
-- Name: lease6 stat_lease6_insert; Type: TRIGGER; Schema: public; Owner: !db_user!
--

CREATE TRIGGER stat_lease6_insert AFTER INSERT ON public.lease6 FOR EACH ROW EXECUTE PROCEDURE public.proc_stat_lease6_insert();


--
-- Name: lease6 stat_lease6_update; Type: TRIGGER; Schema: public; Owner: !db_user!
--

CREATE TRIGGER stat_lease6_update AFTER UPDATE ON public.lease6 FOR EACH ROW EXECUTE PROCEDURE public.proc_stat_lease6_update();


--
-- Name: dhcp4_options fk_dhcp4_option_scode; Type: FK CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.dhcp4_options
    ADD CONSTRAINT fk_dhcp4_option_scode FOREIGN KEY (scope_id) REFERENCES public.dhcp_option_scope(scope_id) ON DELETE CASCADE;


--
-- Name: dhcp6_options fk_dhcp6_option_scode; Type: FK CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.dhcp6_options
    ADD CONSTRAINT fk_dhcp6_option_scode FOREIGN KEY (scope_id) REFERENCES public.dhcp_option_scope(scope_id) ON DELETE CASCADE;


--
-- Name: hosts fk_host_identifier_type; Type: FK CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.hosts
    ADD CONSTRAINT fk_host_identifier_type FOREIGN KEY (dhcp_identifier_type) REFERENCES public.host_identifier_type(type) ON DELETE CASCADE;


--
-- Name: ipv6_reservations fk_ipv6_reservations_host; Type: FK CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.ipv6_reservations
    ADD CONSTRAINT fk_ipv6_reservations_host FOREIGN KEY (host_id) REFERENCES public.hosts(host_id) ON DELETE CASCADE;


--
-- Name: lease4 fk_lease4_state; Type: FK CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.lease4
    ADD CONSTRAINT fk_lease4_state FOREIGN KEY (state) REFERENCES public.lease_state(state);


--
-- Name: lease6 fk_lease6_state; Type: FK CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.lease6
    ADD CONSTRAINT fk_lease6_state FOREIGN KEY (state) REFERENCES public.lease_state(state);


--
-- Name: lease6 fk_lease6_type; Type: FK CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.lease6
    ADD CONSTRAINT fk_lease6_type FOREIGN KEY (lease_type) REFERENCES public.lease6_types(lease_type);


--
-- Name: dhcp4_options fk_options_host1; Type: FK CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.dhcp4_options
    ADD CONSTRAINT fk_options_host1 FOREIGN KEY (host_id) REFERENCES public.hosts(host_id) ON DELETE CASCADE;


--
-- Name: dhcp6_options fk_options_host10; Type: FK CONSTRAINT; Schema: public; Owner: !db_user!
--

ALTER TABLE ONLY public.dhcp6_options
    ADD CONSTRAINT fk_options_host10 FOREIGN KEY (host_id) REFERENCES public.hosts(host_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

