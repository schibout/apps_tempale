-- PostgreSQL 17. Schema consolide issu des migrations Alembic.
-- Revision source : e7a3c15b9f20. Base vide uniquement.
-- Inclut tables, cles, index et extension pg_trgm.

--
-- PostgreSQL database dump
--



SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admin_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.admin_permission (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    permission character varying(50) NOT NULL,
    granted_by uuid,
    granted_at timestamp with time zone NOT NULL
);


--
-- Name: announcement; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.announcement (
    id uuid NOT NULL,
    kind character varying(20) NOT NULL,
    template_key character varying(100),
    variables json NOT NULL,
    translations json NOT NULL,
    level character varying(20) NOT NULL,
    audience character varying(20) NOT NULL,
    role_filter character varying(20),
    show_banner boolean NOT NULL,
    send_email boolean NOT NULL,
    created_by uuid,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: file; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.file (
    id uuid NOT NULL,
    uploaded_by_id uuid,
    url character varying(2048) NOT NULL,
    public_id character varying(512) NOT NULL,
    filename character varying(255),
    content_type character varying(100) NOT NULL,
    size integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    category character varying(40) DEFAULT 'general'::character varying NOT NULL
);


--
-- Name: notification; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.notification (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    type character varying(50) NOT NULL,
    data json NOT NULL,
    read_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: rbac_permission_set; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rbac_permission_set (
    id uuid NOT NULL,
    key character varying(64) NOT NULL,
    name character varying(100) NOT NULL,
    description character varying(255),
    audience character varying(20) NOT NULL,
    is_system boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


--
-- Name: rbac_permission_set_item; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rbac_permission_set_item (
    set_id uuid NOT NULL,
    permission character varying(50) NOT NULL
);


--
-- Name: rbac_role; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rbac_role (
    id uuid NOT NULL,
    key character varying(64) NOT NULL,
    name character varying(100) NOT NULL,
    description character varying(255),
    audience character varying(20) NOT NULL,
    is_system boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


--
-- Name: rbac_role_permission_set; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rbac_role_permission_set (
    role_id uuid NOT NULL,
    set_id uuid NOT NULL
);


--
-- Name: rbac_user_permission_set; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rbac_user_permission_set (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    set_id uuid NOT NULL,
    assigned_by uuid,
    expires_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: rbac_user_role; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rbac_user_role (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    role_id uuid NOT NULL,
    assigned_by uuid,
    expires_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: support_message; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.support_message (
    id uuid NOT NULL,
    ticket_id uuid NOT NULL,
    sender_id uuid,
    sender_role character varying(20) NOT NULL,
    body text NOT NULL,
    read_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: support_message_attachment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.support_message_attachment (
    id uuid NOT NULL,
    message_id uuid NOT NULL,
    file_id uuid NOT NULL,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: support_ticket; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.support_ticket (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    subject character varying(200) NOT NULL,
    status character varying(20) NOT NULL,
    priority character varying(20) NOT NULL,
    assigned_admin_id uuid,
    last_message_at timestamp with time zone NOT NULL,
    closed_at timestamp with time zone,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


--
-- Name: system_setting; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.system_setting (
    id uuid NOT NULL,
    key character varying(100) NOT NULL,
    value text NOT NULL,
    updated_by uuid,
    updated_at timestamp with time zone NOT NULL
);


--
-- Name: user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."user" (
    id uuid NOT NULL,
    email character varying(255) NOT NULL,
    is_active boolean NOT NULL,
    first_name character varying(100),
    last_name character varying(100),
    title character varying(100),
    role character varying(20) NOT NULL,
    hashed_password character varying NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_verified boolean DEFAULT false NOT NULL,
    deactivated_at timestamp with time zone,
    deletion_scheduled_at timestamp with time zone,
    suspended_at timestamp with time zone,
    avatar_file_id uuid,
    is_root_superadmin boolean DEFAULT false NOT NULL
);


--
-- Name: user_activity; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_activity (
    id uuid NOT NULL,
    user_id uuid,
    activity_type character varying NOT NULL,
    resource_type character varying NOT NULL,
    resource_id uuid,
    details json NOT NULL,
    status character varying NOT NULL,
    ip_address character varying,
    user_agent character varying,
    created_at timestamp with time zone NOT NULL,
    status_code integer,
    actor_ref character varying(64),
    user_deleted_at timestamp with time zone
);


--
-- Name: user_mfa; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_mfa (
    user_id uuid NOT NULL,
    secret_encrypted text NOT NULL,
    enabled_at timestamp with time zone,
    last_used_step integer,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: user_mfa_recovery_code; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_mfa_recovery_code (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    code_hash character varying(64) NOT NULL,
    used_at timestamp with time zone
);


--
-- Name: user_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_session (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    refresh_jti character varying(36) NOT NULL,
    user_agent character varying(512),
    ip_address character varying(45),
    created_at timestamp with time zone NOT NULL,
    last_used_at timestamp with time zone NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    revoked_at timestamp with time zone
);


--
-- Name: admin_permission admin_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_permission
    ADD CONSTRAINT admin_permission_pkey PRIMARY KEY (id);


--
-- Name: announcement announcement_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.announcement
    ADD CONSTRAINT announcement_pkey PRIMARY KEY (id);


--
-- Name: file file_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.file
    ADD CONSTRAINT file_pkey PRIMARY KEY (id);


--
-- Name: notification notification_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT notification_pkey PRIMARY KEY (id);


--
-- Name: rbac_permission_set_item rbac_permission_set_item_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_permission_set_item
    ADD CONSTRAINT rbac_permission_set_item_pkey PRIMARY KEY (set_id, permission);


--
-- Name: rbac_permission_set rbac_permission_set_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_permission_set
    ADD CONSTRAINT rbac_permission_set_key_key UNIQUE (key);


--
-- Name: rbac_permission_set rbac_permission_set_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_permission_set
    ADD CONSTRAINT rbac_permission_set_pkey PRIMARY KEY (id);


--
-- Name: rbac_role rbac_role_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_role
    ADD CONSTRAINT rbac_role_key_key UNIQUE (key);


--
-- Name: rbac_role_permission_set rbac_role_permission_set_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_role_permission_set
    ADD CONSTRAINT rbac_role_permission_set_pkey PRIMARY KEY (role_id, set_id);


--
-- Name: rbac_role rbac_role_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_role
    ADD CONSTRAINT rbac_role_pkey PRIMARY KEY (id);


--
-- Name: rbac_user_permission_set rbac_user_permission_set_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_user_permission_set
    ADD CONSTRAINT rbac_user_permission_set_pkey PRIMARY KEY (id);


--
-- Name: rbac_user_role rbac_user_role_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_user_role
    ADD CONSTRAINT rbac_user_role_pkey PRIMARY KEY (id);


--
-- Name: support_message_attachment support_message_attachment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_message_attachment
    ADD CONSTRAINT support_message_attachment_pkey PRIMARY KEY (id);


--
-- Name: support_message support_message_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_message
    ADD CONSTRAINT support_message_pkey PRIMARY KEY (id);


--
-- Name: support_ticket support_ticket_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_ticket
    ADD CONSTRAINT support_ticket_pkey PRIMARY KEY (id);


--
-- Name: system_setting system_setting_key_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.system_setting
    ADD CONSTRAINT system_setting_key_key UNIQUE (key);


--
-- Name: system_setting system_setting_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.system_setting
    ADD CONSTRAINT system_setting_pkey PRIMARY KEY (id);


--
-- Name: admin_permission uq_admin_permission_user_perm; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_permission
    ADD CONSTRAINT uq_admin_permission_user_perm UNIQUE (user_id, permission);


--
-- Name: rbac_user_permission_set uq_rbac_user_permission_set; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_user_permission_set
    ADD CONSTRAINT uq_rbac_user_permission_set UNIQUE (user_id, set_id);


--
-- Name: rbac_user_role uq_rbac_user_role_user_role; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_user_role
    ADD CONSTRAINT uq_rbac_user_role_user_role UNIQUE (user_id, role_id);


--
-- Name: support_message_attachment uq_support_attachment_message_file; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_message_attachment
    ADD CONSTRAINT uq_support_attachment_message_file UNIQUE (message_id, file_id);


--
-- Name: user_activity user_activity_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_activity
    ADD CONSTRAINT user_activity_pkey PRIMARY KEY (id);


--
-- Name: user_mfa user_mfa_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_mfa
    ADD CONSTRAINT user_mfa_pkey PRIMARY KEY (user_id);


--
-- Name: user_mfa_recovery_code user_mfa_recovery_code_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_mfa_recovery_code
    ADD CONSTRAINT user_mfa_recovery_code_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user_session user_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_session
    ADD CONSTRAINT user_session_pkey PRIMARY KEY (id);


--
-- Name: ix_admin_permission_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_admin_permission_user_id ON public.admin_permission USING btree (user_id);


--
-- Name: ix_announcement_banner_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_announcement_banner_created ON public.announcement USING btree (show_banner, created_at);


--
-- Name: ix_announcement_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_announcement_created ON public.announcement USING btree (created_at);


--
-- Name: ix_file_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_file_category ON public.file USING btree (category);


--
-- Name: ix_file_uploaded_by_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_file_uploaded_by_id ON public.file USING btree (uploaded_by_id);


--
-- Name: ix_notification_user_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_notification_user_created ON public.notification USING btree (user_id, created_at);


--
-- Name: ix_rbac_role_permission_set_set_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_rbac_role_permission_set_set_id ON public.rbac_role_permission_set USING btree (set_id);


--
-- Name: ix_rbac_user_permission_set_set_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_rbac_user_permission_set_set_id ON public.rbac_user_permission_set USING btree (set_id);


--
-- Name: ix_rbac_user_role_role_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_rbac_user_role_role_id ON public.rbac_user_role USING btree (role_id);


--
-- Name: ix_support_message_attachment_message_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_support_message_attachment_message_id ON public.support_message_attachment USING btree (message_id);


--
-- Name: ix_support_message_ticket_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_support_message_ticket_created ON public.support_message USING btree (ticket_id, created_at);


--
-- Name: ix_support_ticket_status_last_message; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_support_ticket_status_last_message ON public.support_ticket USING btree (status, last_message_at);


--
-- Name: ix_support_ticket_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_support_ticket_user_id ON public.support_ticket USING btree (user_id);


--
-- Name: ix_user_activity_activity_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_activity_activity_type ON public.user_activity USING btree (activity_type);


--
-- Name: ix_user_activity_actor_ref; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_activity_actor_ref ON public.user_activity USING btree (actor_ref);


--
-- Name: ix_user_activity_created_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_activity_created_at ON public.user_activity USING btree (created_at);


--
-- Name: ix_user_activity_resource_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_activity_resource_id ON public.user_activity USING btree (resource_id);


--
-- Name: ix_user_activity_resource_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_activity_resource_type ON public.user_activity USING btree (resource_type);


--
-- Name: ix_user_activity_user_deleted_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_activity_user_deleted_at ON public.user_activity USING btree (user_deleted_at);


--
-- Name: ix_user_activity_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_activity_user_id ON public.user_activity USING btree (user_id);


--
-- Name: ix_user_deletion_due; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_deletion_due ON public."user" USING btree (deletion_scheduled_at) WHERE ((is_active = false) AND (deletion_scheduled_at IS NOT NULL));


--
-- Name: ix_user_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);


--
-- Name: ix_user_email_trgm; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_email_trgm ON public."user" USING gin (email public.gin_trgm_ops);


--
-- Name: ix_user_first_name_trgm; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_first_name_trgm ON public."user" USING gin (first_name public.gin_trgm_ops);


--
-- Name: ix_user_last_name_trgm; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_last_name_trgm ON public."user" USING gin (last_name public.gin_trgm_ops);


--
-- Name: ix_user_mfa_recovery_code_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_mfa_recovery_code_user_id ON public.user_mfa_recovery_code USING btree (user_id);


--
-- Name: ix_user_session_expires_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_session_expires_at ON public.user_session USING btree (expires_at);


--
-- Name: ix_user_session_user_last_used; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_user_session_user_last_used ON public.user_session USING btree (user_id, last_used_at);


--
-- Name: admin_permission admin_permission_granted_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_permission
    ADD CONSTRAINT admin_permission_granted_by_fkey FOREIGN KEY (granted_by) REFERENCES public."user"(id) ON DELETE SET NULL;


--
-- Name: admin_permission admin_permission_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.admin_permission
    ADD CONSTRAINT admin_permission_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- Name: announcement announcement_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.announcement
    ADD CONSTRAINT announcement_created_by_fkey FOREIGN KEY (created_by) REFERENCES public."user"(id) ON DELETE SET NULL;


--
-- Name: file file_uploaded_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.file
    ADD CONSTRAINT file_uploaded_by_id_fkey FOREIGN KEY (uploaded_by_id) REFERENCES public."user"(id) ON DELETE SET NULL;


--
-- Name: user fk_user_avatar_file_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT fk_user_avatar_file_id FOREIGN KEY (avatar_file_id) REFERENCES public.file(id) ON DELETE SET NULL;


--
-- Name: notification notification_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT notification_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- Name: rbac_permission_set_item rbac_permission_set_item_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_permission_set_item
    ADD CONSTRAINT rbac_permission_set_item_set_id_fkey FOREIGN KEY (set_id) REFERENCES public.rbac_permission_set(id) ON DELETE CASCADE;


--
-- Name: rbac_role_permission_set rbac_role_permission_set_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_role_permission_set
    ADD CONSTRAINT rbac_role_permission_set_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.rbac_role(id) ON DELETE CASCADE;


--
-- Name: rbac_role_permission_set rbac_role_permission_set_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_role_permission_set
    ADD CONSTRAINT rbac_role_permission_set_set_id_fkey FOREIGN KEY (set_id) REFERENCES public.rbac_permission_set(id) ON DELETE RESTRICT;


--
-- Name: rbac_user_permission_set rbac_user_permission_set_assigned_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_user_permission_set
    ADD CONSTRAINT rbac_user_permission_set_assigned_by_fkey FOREIGN KEY (assigned_by) REFERENCES public."user"(id) ON DELETE SET NULL;


--
-- Name: rbac_user_permission_set rbac_user_permission_set_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_user_permission_set
    ADD CONSTRAINT rbac_user_permission_set_set_id_fkey FOREIGN KEY (set_id) REFERENCES public.rbac_permission_set(id) ON DELETE RESTRICT;


--
-- Name: rbac_user_permission_set rbac_user_permission_set_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_user_permission_set
    ADD CONSTRAINT rbac_user_permission_set_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- Name: rbac_user_role rbac_user_role_assigned_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_user_role
    ADD CONSTRAINT rbac_user_role_assigned_by_fkey FOREIGN KEY (assigned_by) REFERENCES public."user"(id) ON DELETE SET NULL;


--
-- Name: rbac_user_role rbac_user_role_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_user_role
    ADD CONSTRAINT rbac_user_role_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.rbac_role(id) ON DELETE RESTRICT;


--
-- Name: rbac_user_role rbac_user_role_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rbac_user_role
    ADD CONSTRAINT rbac_user_role_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- Name: support_message_attachment support_message_attachment_file_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_message_attachment
    ADD CONSTRAINT support_message_attachment_file_id_fkey FOREIGN KEY (file_id) REFERENCES public.file(id) ON DELETE CASCADE;


--
-- Name: support_message_attachment support_message_attachment_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_message_attachment
    ADD CONSTRAINT support_message_attachment_message_id_fkey FOREIGN KEY (message_id) REFERENCES public.support_message(id) ON DELETE CASCADE;


--
-- Name: support_message support_message_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_message
    ADD CONSTRAINT support_message_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public."user"(id) ON DELETE SET NULL;


--
-- Name: support_message support_message_ticket_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_message
    ADD CONSTRAINT support_message_ticket_id_fkey FOREIGN KEY (ticket_id) REFERENCES public.support_ticket(id) ON DELETE CASCADE;


--
-- Name: support_ticket support_ticket_assigned_admin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_ticket
    ADD CONSTRAINT support_ticket_assigned_admin_id_fkey FOREIGN KEY (assigned_admin_id) REFERENCES public."user"(id) ON DELETE SET NULL;


--
-- Name: support_ticket support_ticket_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.support_ticket
    ADD CONSTRAINT support_ticket_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- Name: system_setting system_setting_updated_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.system_setting
    ADD CONSTRAINT system_setting_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES public."user"(id) ON DELETE SET NULL;


--
-- Name: user_activity user_activity_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_activity
    ADD CONSTRAINT user_activity_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE SET NULL;


--
-- Name: user_mfa_recovery_code user_mfa_recovery_code_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_mfa_recovery_code
    ADD CONSTRAINT user_mfa_recovery_code_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- Name: user_mfa user_mfa_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_mfa
    ADD CONSTRAINT user_mfa_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- Name: user_session user_session_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_session
    ADD CONSTRAINT user_session_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--
