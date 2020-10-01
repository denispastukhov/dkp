select_guilds = """select * from servers where discord_id = %s"""

insert_guild = """ INSERT INTO public.servers(
         discord_id, discord_name)
         VALUES (%s, %s);
         """

select_users = """ select * from public.users where server_id = (select id from public.servers where discord_id = %s) and user_id = %s"""
insert_user = """INSERT INTO public.users(
	username, user_id, server_id)
	VALUES (%s, %s, (select id from public.servers where discord_id = %s)); """

select_active_periods = "select * from public.payment_periods where server_id = (select id from public.servers where discord_id = %s) and close_date is null"
insert_active_period = """INSERT INTO public.payment_periods(
	open_date, payment, server_id, close_date)
	VALUES ( now(), null, (select id from public.servers where discord_id = %s), null);"""
select_periods = "select * from public.payment_periods where server_id = (select id from public.servers where discord_id = %s)"
update_close_period = """UPDATE public.payment_periods
	SET payment=%s, close_date=now()
	WHERE id = %s;"""
select_validation_id = "select max(validation_id) from public.user_points where period_id = %s"

# init_scripts = 
# CREATE TABLE public.servers
# (
#     id integer NOT NULL DEFAULT nextval('servers_id_seq'::regclass),
#     discord_id bigint NOT NULL,
#     discord_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
#     CONSTRAINT servers_pkey PRIMARY KEY (id),
#     CONSTRAINT discord_id_unique UNIQUE (discord_id)
# )
# CREATE TABLE public.user_points
# (
#     id integer NOT NULL DEFAULT nextval('user_points_id_seq'::regclass),
#     user_id integer NOT NULL,
#     period_id integer NOT NULL,
#     validated boolean NOT NULL,
#     add_date timestamp without time zone NOT NULL DEFAULT now(),
#     points integer NOT NULL DEFAULT 0,
#     CONSTRAINT points_pkey PRIMARY KEY (id),
#     CONSTRAINT points_period_id FOREIGN KEY (period_id)
#         REFERENCES public.payment_periods (id) MATCH SIMPLE
#         ON UPDATE NO ACTION
#         ON DELETE NO ACTION,
#     CONSTRAINT points_users_id FOREIGN KEY (user_id)
#         REFERENCES public.users (id) MATCH SIMPLE
#         ON UPDATE NO ACTION
#         ON DELETE NO ACTION
# )
# CREATE TABLE public.users
# (
#     id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
#     username character varying(80) COLLATE pg_catalog."default" NOT NULL,
#     register_date timestamp without time zone DEFAULT now(),
#     server_id integer NOT NULL,
#     deleted boolean DEFAULT false,
#     user_id bigint NOT NULL,
#     CONSTRAINT person_pkey PRIMARY KEY (id),
#     CONSTRAINT serverid_userid_unique UNIQUE (server_id, user_id),
#     CONSTRAINT user_server_fkey FOREIGN KEY (server_id)
#         REFERENCES public.servers (id) MATCH SIMPLE
#         ON UPDATE NO ACTION
#         ON DELETE NO ACTION
#         NOT VALID
# )
# CREATE TABLE public.payment_periods
# (
#     id integer NOT NULL DEFAULT nextval('payment_periods_id_seq'::regclass),
#     open_date timestamp without time zone NOT NULL,
#     payment money,
#     server_id integer NOT NULL,
#     close_date timestamp without time zone,
#     CONSTRAINT payment_pkey PRIMARY KEY (id),
#     CONSTRAINT serverid_servers FOREIGN KEY (server_id)
#         REFERENCES public.servers (id) MATCH SIMPLE
#         ON UPDATE NO ACTION
#         ON DELETE NO ACTION
#         NOT VALID
# )