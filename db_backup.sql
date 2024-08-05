--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3 (Debian 16.3-1.pgdg120+1)
-- Dumped by pg_dump version 16.3 (Debian 16.3-1.pgdg120+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: app_user; Type: TABLE; Schema: public; Owner: myuser
--

CREATE TABLE public.app_user (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    username character varying(120) NOT NULL
);


ALTER TABLE public.app_user OWNER TO myuser;

--
-- Name: app_user_id_seq; Type: SEQUENCE; Schema: public; Owner: myuser
--

CREATE SEQUENCE public.app_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.app_user_id_seq OWNER TO myuser;

--
-- Name: app_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: myuser
--

ALTER SEQUENCE public.app_user_id_seq OWNED BY public.app_user.id;


--
-- Name: app_user id; Type: DEFAULT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.app_user ALTER COLUMN id SET DEFAULT nextval('public.app_user_id_seq'::regclass);


--
-- Data for Name: app_user; Type: TABLE DATA; Schema: public; Owner: myuser
--

COPY public.app_user (id, name, username) FROM stdin;
1	userPython1	userPython1
3	userPython2	userPython2
7	userPython4	userPython4
10	userPython5	userPython5
12	userPython6	userPython6
14	userPython7	userPython7
17	userPython8	userPython8
19	userPython9	userPython9
21	userPython10	userPython10
24	userPython11	userPython11
27	userPython12	userPython12
29	userPython13	userPython13
31	userPython14	userPython14
33	userPython15	userPython15
37	userPython17	userPython17
39	userPython18	userPython18
41	userPython19	userPython19
43	userPython20	userPython20
47	userPython21	userPython21
49	userPython22	userPython22
51	userPython23	userPython23
53	userPython24	userPython24
55	userPython25	userPython25
57	userPython26	userPython26
59	userPython27	userPython27
62	userPython28	userPython28
64	userPython29	userPython29
66	userPython30	userPython30
70	userPython31	userPython31
72	userPython32	userPython32
73	userPython33	userPython33
2	userJava1	userJava1
4	userJava2	userJava2
6	userJava3	userJava3
8	userJava4	userJava4
9	userJava5	userJava5
11	userJava6	userJava6
13	userJava7	userJava7
16	userJava9	userJava9
18	userJava10	userJava10
20	userJava11	userJava11
22	userJava12	userJava12
23	userJava13	userJava13
26	userJava15	userJava15
28	userJava16	userJava16
30	userJava17	userJava17
32	userJava18	userJava18
34	userJava19	userJava19
36	userJava20	userJava20
38	userJava21	userJava21
40	userJava22	userJava22
42	userJava23	userJava23
44	userJava24	userJava24
45	userJava25	userJava25
46	userJava26	userJava26
48	userJava27	userJava27
50	userJava28	userJava28
52	userJava29	userJava29
54	userJava30	userJava30
56	userJava31	userJava31
58	userJava32	userJava32
60	userJava33	userJava33
61	userJava34	userJava34
63	userJava35	userJava35
65	userJava36	userJava36
67	userJava37	userJava37
68	userJava38	userJava38
69	userJava39	userJava39
71	userJava40	userJava40
74	userJava41	userJava41
\.


--
-- Name: app_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: myuser
--

SELECT pg_catalog.setval('public.app_user_id_seq', 89, true);


--
-- Name: app_user app_user_pkey; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.app_user
    ADD CONSTRAINT app_user_pkey PRIMARY KEY (id);


--
-- Name: app_user app_user_username_key; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.app_user
    ADD CONSTRAINT app_user_username_key UNIQUE (username);


--
-- PostgreSQL database dump complete
--

