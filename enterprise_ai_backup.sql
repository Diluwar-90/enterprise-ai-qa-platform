--
-- PostgreSQL database dump
--

\restrict laXEAouj5kunF6LhzdzPMISlNHJgvIokGr9HY0IIqWLf6lqOfnZwufxyfP51ay0

-- Dumped from database version 15.15 (Homebrew)
-- Dumped by pg_dump version 15.15 (Homebrew)

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: diluwar
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO diluwar;

--
-- Name: document_chunks; Type: TABLE; Schema: public; Owner: diluwar
--

CREATE TABLE public.document_chunks (
    id uuid NOT NULL,
    document_id uuid NOT NULL,
    chunk_index integer NOT NULL,
    content text NOT NULL,
    token_count integer,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.document_chunks OWNER TO diluwar;

--
-- Name: documents; Type: TABLE; Schema: public; Owner: diluwar
--

CREATE TABLE public.documents (
    id uuid NOT NULL,
    owner_id uuid NOT NULL,
    filename character varying(255) NOT NULL,
    content_type character varying(100) NOT NULL,
    file_size integer NOT NULL,
    status character varying(30) NOT NULL,
    storage_path character varying(500) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    error_message text,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.documents OWNER TO diluwar;

--
-- Name: users; Type: TABLE; Schema: public; Owner: diluwar
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    email character varying(255) NOT NULL,
    full_name character varying(255) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.users OWNER TO diluwar;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: diluwar
--

COPY public.alembic_version (version_num) FROM stdin;
1b9ac79a7463
\.


--
-- Data for Name: document_chunks; Type: TABLE DATA; Schema: public; Owner: diluwar
--

COPY public.document_chunks (id, document_id, chunk_index, content, token_count, created_at) FROM stdin;
38ccc82a-b7c8-4267-9e6d-1dc4a72c2944	6a6dd3b4-b163-4b82-8559-8016956f17b3	0	Enterprise AI Knowledge Platform test document.	\N	2026-08-09 12:15:37.44067+05:30
9fbf086a-2e74-4bb3-862e-1c748a244e12	3f54894b-7b6b-4fb6-bde7-e7c0988a224b	0	Enterprise Knowledge Intelligence Platform test content.	\N	2026-08-09 12:26:10.748673+05:30
66062731-21a0-4648-97b8-39183a2bdaa7	3645bffe-8e09-4cd1-ae15-30b264bf5660	0	Enterprise Knowledge Intelligence Platform test content.	\N	2026-08-09 12:34:36.472077+05:30
786f7ead-718c-437f-8600-07d2b8fe98e5	81e8c710-3399-4433-8937-8fad79029da7	0	Enterprise AI Knowledge Platform test document.	\N	2026-08-09 12:35:21.329302+05:30
f8eb9f09-eedf-4f25-99c2-cd15121f4338	7d3a6650-fb13-4e5a-b057-2856b3b38146	0	Enterprise Knowledge Intelligence Platform test content.	\N	2026-08-09 12:41:15.735319+05:30
fe35de53-3bc2-4c08-946c-29bf83fb9bf3	f574a9c5-2673-4a66-b094-6215bb0439de	0	Enterprise Knowledge Intelligence Platform test content.	\N	2026-08-09 12:43:29.227094+05:30
aad353b6-3865-4991-8ab3-8d8fc78e7fcc	5f3d4301-934a-4369-94e1-b09a0e5ff7ea	0	Enterprise Knowledge Intelligence Platform test content.	\N	2026-08-10 19:46:49.097234+05:30
\.


--
-- Data for Name: documents; Type: TABLE DATA; Schema: public; Owner: diluwar
--

COPY public.documents (id, owner_id, filename, content_type, file_size, status, storage_path, created_at, error_message, updated_at) FROM stdin;
6e19cc49-5369-4f47-a99c-229b8555d248	11111111-1111-1111-1111-111111111111	test.txt	text/plain	48	uploaded	storage/documents/6e19cc49-5369-4f47-a99c-229b8555d248/test.txt	2026-08-09 11:43:19.158852+05:30	\N	2026-08-09 11:43:19.158857+05:30
6a6dd3b4-b163-4b82-8559-8016956f17b3	11111111-1111-1111-1111-111111111111	test.txt	text/plain	48	processed	storage/documents/6a6dd3b4-b163-4b82-8559-8016956f17b3/test.txt	2026-08-09 12:15:37.384888+05:30	\N	2026-08-09 12:15:37.411531+05:30
3f54894b-7b6b-4fb6-bde7-e7c0988a224b	9be1c5dd-0114-4287-996b-47c25b453e68	test.txt	text/plain	56	processed	/private/var/folders/yd/506k_7vj1cg2bsp87dqc_sx00000gn/T/pytest-of-diluwar/pytest-5/test_process_text_document0/test.txt	2026-08-09 12:26:10.742129+05:30	\N	2026-08-09 12:26:10.746946+05:30
3645bffe-8e09-4cd1-ae15-30b264bf5660	cc4704f2-49d8-4a46-bae6-249d53fd6d3e	test.txt	text/plain	56	processed	/private/var/folders/yd/506k_7vj1cg2bsp87dqc_sx00000gn/T/pytest-of-diluwar/pytest-6/test_process_text_document0/test.txt	2026-08-09 12:34:36.458336+05:30	\N	2026-08-09 12:34:36.466358+05:30
81e8c710-3399-4433-8937-8fad79029da7	11111111-1111-1111-1111-111111111111	test.txt	text/plain	48	processed	storage/documents/81e8c710-3399-4433-8937-8fad79029da7/test.txt	2026-08-09 12:35:21.287982+05:30	\N	2026-08-09 12:35:21.326851+05:30
7d3a6650-fb13-4e5a-b057-2856b3b38146	96b922c4-c139-4b29-9871-9fe5d455fea9	test.txt	text/plain	56	processed	/private/var/folders/yd/506k_7vj1cg2bsp87dqc_sx00000gn/T/pytest-of-diluwar/pytest-7/test_process_text_document0/test.txt	2026-08-09 12:41:15.7236+05:30	\N	2026-08-09 12:41:15.732861+05:30
f574a9c5-2673-4a66-b094-6215bb0439de	a84efd65-8d41-4da1-ac8c-7c7eee7fff09	test.txt	text/plain	56	processed	/private/var/folders/yd/506k_7vj1cg2bsp87dqc_sx00000gn/T/pytest-of-diluwar/pytest-8/test_process_text_document0/test.txt	2026-08-09 12:43:29.216016+05:30	\N	2026-08-09 12:43:29.224077+05:30
5f3d4301-934a-4369-94e1-b09a0e5ff7ea	00abd734-7a38-4c6d-9049-897efb1dbd1b	test.txt	text/plain	56	processed	/private/var/folders/yd/506k_7vj1cg2bsp87dqc_sx00000gn/T/pytest-of-diluwar/pytest-9/test_process_text_document0/test.txt	2026-08-10 19:46:49.079429+05:30	\N	2026-08-10 19:46:49.0935+05:30
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: diluwar
--

COPY public.users (id, email, full_name, is_active, created_at) FROM stdin;
11111111-1111-1111-1111-111111111111	test@example.com	Test User	t	2026-08-09 17:10:26.551468+05:30
9be1c5dd-0114-4287-996b-47c25b453e68	test-fd202577-c0aa-4c6a-8bba-622b4975645c@example.com	Test User	t	2026-08-09 12:26:10.73439+05:30
cc4704f2-49d8-4a46-bae6-249d53fd6d3e	test-3034d639-5643-4f73-b98d-2adde8037559@example.com	Test User	t	2026-08-09 12:34:36.450534+05:30
96b922c4-c139-4b29-9871-9fe5d455fea9	test-3511f9c9-e074-49a9-93fe-e59a0fe3297b@example.com	Test User	t	2026-08-09 12:41:15.714746+05:30
a84efd65-8d41-4da1-ac8c-7c7eee7fff09	test-5605cda8-7797-438a-9bee-0a7feaff3bcc@example.com	Test User	t	2026-08-09 12:43:29.207569+05:30
00abd734-7a38-4c6d-9049-897efb1dbd1b	test-c4d783e8-5cb7-4d3d-a6d5-b715f6829e40@example.com	Test User	t	2026-08-10 19:46:49.064787+05:30
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: diluwar
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: document_chunks document_chunks_pkey; Type: CONSTRAINT; Schema: public; Owner: diluwar
--

ALTER TABLE ONLY public.document_chunks
    ADD CONSTRAINT document_chunks_pkey PRIMARY KEY (id);


--
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: diluwar
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: diluwar
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_document_chunks_document_id; Type: INDEX; Schema: public; Owner: diluwar
--

CREATE INDEX ix_document_chunks_document_id ON public.document_chunks USING btree (document_id);


--
-- Name: ix_documents_owner_id; Type: INDEX; Schema: public; Owner: diluwar
--

CREATE INDEX ix_documents_owner_id ON public.documents USING btree (owner_id);


--
-- Name: ix_documents_status; Type: INDEX; Schema: public; Owner: diluwar
--

CREATE INDEX ix_documents_status ON public.documents USING btree (status);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: diluwar
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: document_chunks document_chunks_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: diluwar
--

ALTER TABLE ONLY public.document_chunks
    ADD CONSTRAINT document_chunks_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.documents(id) ON DELETE CASCADE;


--
-- Name: documents documents_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: diluwar
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict laXEAouj5kunF6LhzdzPMISlNHJgvIokGr9HY0IIqWLf6lqOfnZwufxyfP51ay0

