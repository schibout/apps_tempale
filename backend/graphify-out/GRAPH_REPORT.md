# Graph Report - backend  (2026-11-07)

## Corpus Check
- 233 files · ~116,758 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 5, .ini 2, .example 1)

## Summary
- 4067 nodes · 12659 edges · 177 communities (89 shown, 88 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 761 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ad9183b0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- tests/test_files.py
- AsyncClient
- User
- admin/user_service.py
- rbac_service.py
- utc_now
- Permission
- admin/support_service.py
- Email Tokens and Success Messages
- test_mfa_flow.py
- test_rbac_effective.py
- test_rbac.py
- make_client
- FileCategory
- Broadcast Notification Tests
- test_scrub_audit_migration.py
- AsyncClient
- auth.py
- admin/file_service.py
- Configuration and Email Services
- test_sessions.py
- user_has_permission
- test_notify_hooks.py
- Announcement
- list_my_tickets
- services/support_service.py
- notify.py
- _filtered_tickets_stmt
- config.py
- Notification
- get_redis
- list_broadcasts
- Language
- lifespan.py
- serve_account_socket
- is_login_locked
- broadcast_templates.py
- broadcast_service.py
- notifications.py
- _account
- _role_payload
- _assign_set
- env.py
- user_mfa.py
- list_tickets
- get_stats
- sqlalchemy
- auth_service.py
- test_rbac_bootstrap.py
- repositories/user.py
- announcements.py
- get_current_user
- StubSocket
- routes/health.py
- storage.py
- test_redis_failure_falls_back_to_database_and_never_grants
- API Exception Handlers
- Settings
- watch_socket
- test_realtime.py
- Admin File Tests
- SystemRole
- ActiveUser
- register_and_verify
- use_cases/settings.py
- test_metrics.py
- make_user_client
- _grant
- UserActivity
- _BrokenPipeline
- system_settings_service.py
- test_rbac_route_coverage.py
- Origin Restriction Tests
- user_topic
- make_user_client
- rate_limit.py
- user_agent.py
- _find_kwarg
- mfa_service.py
- security.py
- repositories/rbac.py
- StubWebSocket
- a48b0bc6e988_add_ondelete_cascade_on_user_activity_fk.py
- other_client
- list_user_activities
- _SafeDict
- VariableType
- reset_mfa.py
- test_rbac_user_routes.py
- log_activity
- test_rbac_api.py
- test_admin_socket_serves_a_session_with_mfa_claim
- update_system_setting
- User
- _make_user
- test_log_activity_defaults_success_status_code_to_200
- ensure_utc
- test_set_admin_permissions_rejects_self_keys
- test_permission_change_publishes_realtime_event
- test_maintenance_gate_blocks_admin_without_mfa_claim
- db_session
- telemetry.py
- services/user_service.py
- ErrorMessages
- user_has_permission
- app/main.py
- test_health.py

## God Nodes (most connected - your core abstractions)
1. `User` - 234 edges
2. `ErrorMessages` - 172 edges
3. `SystemRole` - 132 edges
4. `register_and_verify()` - 128 edges
5. `Permission` - 116 edges
6. `get_user_id()` - 111 edges
7. `utc_now()` - 103 edges
8. `audit_unexpected_failure()` - 86 edges
9. `log_activity()` - 84 edges
10. `SuccessMessages` - 62 edges

## Surprising Connections (you probably didn't know these)
- `User` --calls--> `seed()`  [EXTRACTED]
  app/models/user.py → loadtest/seed_users.py
- `seed()` --calls--> `get_user_by_email()`  [EXTRACTED]
  loadtest/seed_users.py → app/repositories/user.py
- `seed()` --calls--> `create_user()`  [EXTRACTED]
  loadtest/seed_users.py → app/repositories/user.py
- `Permission` --uses--> `test_permission_change_publishes_realtime_event()`  [INFERRED]
  app/schemas/admin_permission.py → app/tests/admin/test_realtime_permissions.py
- `Permission` --uses--> `test_admin_lists_and_revokes_user_sessions()`  [INFERRED]
  app/schemas/admin_permission.py → app/tests/test_sessions.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **FastAPI Template Tech Stack** — uv_package_manager, app_core, app_models, app_worker [EXTRACTED 1.00]
- **Architecture Dependency Flow** — app_api_routes, app_services, app_repositories, app_models [EXTRACTED 1.00]

## Communities (177 total, 88 thin omitted)

### Community 0 - "tests/test_files.py"
Cohesion: 0.05
Nodes (34): test_control_characters_and_null_bytes_removed(), test_custom_max_length_is_respected(), test_empty_after_sanitizing_falls_back(), test_injection_characters_are_replaced(), test_leading_dots_are_trimmed(), test_long_name_truncated_within_limit_keeping_extension(), test_none_passes_through(), test_path_components_are_stripped() (+26 more)

### Community 1 - "AsyncClient"
Cohesion: 0.11
Nodes (13): _enable_maintenance(), test_list_settings_returns_registry(), test_maintenance_allows_admin(), test_maintenance_blocks_anonymous(), test_maintenance_blocks_regular_user(), test_maintenance_exempts_login(), test_maintenance_exempts_public_settings(), test_patch_invalid_value_returns_422() (+5 more)

### Community 2 - "User"
Cohesion: 0.12
Nodes (10): _ensure_root_designated(), _filtered_users_stmt(), get_earliest_superadmin(), is_last_active_admin(), is_last_active_superadmin(), list_admins(), list_users_admin(), root_superadmin_exists() (+2 more)

### Community 3 - "admin/user_service.py"
Cohesion: 0.05
Nodes (37): change_user_password(), delete_user(), get_user(), list_user_sessions(), list_users(), reset_user_mfa(), revoke_user_sessions(), suspend_user() (+29 more)

### Community 4 - "rbac_service.py"
Cohesion: 0.03
Nodes (95): create_permission_set_endpoint(), create_role_endpoint(), delete_permission_set_endpoint(), delete_role_endpoint(), get_permission_set_endpoint(), get_role_endpoint(), get_user_access_endpoint(), list_permission_sets_endpoint() (+87 more)

### Community 5 - "utc_now"
Cohesion: 0.11
Nodes (14): _entry(), _set_id(), _store_set_assignment(), test_access_names_the_source_of_each_key(), test_assignment_invalidates_and_publishes(), test_assignment_needs_the_keys(), test_expired_admin_row_does_not_promote(), test_expired_row_may_be_resent_or_dropped_without_its_keys() (+6 more)

### Community 6 - "Permission"
Cohesion: 0.04
Nodes (39): require_user_permission(), SystemPermissionSetDefinition, SystemRoleDefinition, get_permissions_for_users(), set_user_permissions(), stage_user_permissions(), get_next_assignment_expiry(), directly_grantable_permissions() (+31 more)

### Community 7 - "admin/support_service.py"
Cohesion: 0.08
Nodes (24): publish_feeds(), publish_safe(), AdminTicketDetail, AdminTicketListItem, AdminTicketListResponse, AdminTicketResponse, AdminTicketUpdate, MessageCreate (+16 more)

### Community 8 - "Email Tokens and Success Messages"
Cohesion: 0.15
Nodes (11): auth_client(), test_deactivated_user_blocked_from_update(), test_delete_user_me_schedules_deletion(), test_delete_user_me_twice_returns_400(), test_delete_user_me_wrong_password_rejected(), test_me_exposes_deletion_schedule(), test_reactivate_cancels_deletion(), test_reactivate_on_active_account_returns_400() (+3 more)

### Community 9 - "test_mfa_flow.py"
Cohesion: 0.05
Nodes (51): access_claims(), assert_lists_admin_keys(), audit_rows(), create_admin(), enroll(), mfa_row(), open_admin_session(), post_login() (+43 more)

### Community 11 - "test_rbac_effective.py"
Cohesion: 0.18
Nodes (6): _role_id(), _set_id(), test_deleting_the_assigning_admin_clears_assigned_by(), test_set_added_to_a_role_shows_after_global_invalidation(), test_unknown_stored_permission_key_is_skipped(), invalidate_all_permissions()

### Community 13 - "test_rbac.py"
Cohesion: 0.04
Nodes (74): _account_exists(), _assign_role(), _assign_set(), _assigned_role_keys(), _assigned_set_keys(), _call_user_route(), _direct_grants(), _expect_policy_close() (+66 more)

### Community 14 - "make_client"
Cohesion: 0.10
Nodes (13): make_client(), root(), test_access_of_a_superadmin_shows_every_key(), test_connected_account_sees_a_role_assignment_at_once(), test_delegate_with_admins_write_promotes(), test_direct_grant_editor_keeps_an_admin_with_a_role(), test_permission_catalog_needs_roles_read(), test_permission_catalog_needs_roles_read_or_permission_sets_read() (+5 more)

### Community 15 - "FileCategory"
Cohesion: 0.12
Nodes (4): upload_file(), FileCategory, FilePublic, resolve_attachment_files()

### Community 16 - "Broadcast Notification Tests"
Cohesion: 0.09
Nodes (19): _announcement_notifications(), _notification_count(), test_active_banner_absent_returns_null(), test_create_active_audience_targets_active_users(), test_create_custom_broadcast(), test_create_custom_with_template_key_is_rejected(), test_create_custom_without_translations_is_rejected(), test_create_forbidden_for_regular_user() (+11 more)

### Community 17 - "test_scrub_audit_migration.py"
Cohesion: 0.18
Nodes (4): _load_rbac_migration(), test_migration_uses_the_catalog_default_role_id(), _load_migration(), test_scrub_rewrites_only_the_targeted_rows()

### Community 18 - "AsyncClient"
Cohesion: 0.13
Nodes (13): _assignments(), _set_keys(), test_assignment_opens_then_withdrawal_closes_the_panel(), test_demotion_keeps_user_audience_assignments(), test_edit_of_a_keyless_last_admin_is_refused(), test_edit_repairs_an_admin_without_admin_access(), test_expired_access_does_not_keep_the_tier(), test_last_active_admin_cannot_lose_its_last_access() (+5 more)

### Community 19 - "auth.py"
Cohesion: 0.05
Nodes (40): audit_unexpected_failure(), change_password(), _clear_auth_cookies(), forgot_password(), login_access_token(), logout(), mfa_enroll_confirm(), mfa_enroll_start() (+32 more)

### Community 20 - "admin/file_service.py"
Cohesion: 0.11
Nodes (9): delete_file(), get_file(), list_files(), AdminFileListItem, AdminFileListResponse, delete_file_admin_service(), get_file_admin_service(), list_files_admin_service() (+1 more)

### Community 21 - "Configuration and Email Services"
Cohesion: 0.14
Nodes (13): check_mx_record(), _get_domain(), is_disposable_email(), reset_disposable_cache(), test_check_mx_record_invalid(), test_check_mx_record_valid(), test_is_disposable_email_false(), test_is_disposable_email_fetch_error() (+5 more)

### Community 22 - "test_sessions.py"
Cohesion: 0.19
Nodes (17): _fresh_client(), _insert_session(), _login(), test_admin_lists_and_revokes_user_sessions(), test_admin_sessions_require_permission(), test_change_password_revokes_every_session(), test_list_sessions_pagination(), test_login_creates_session_with_device_metadata() (+9 more)

### Community 23 - "user_has_permission"
Cohesion: 0.15
Nodes (10): ensure_permission(), _request_body_fields(), require_any_permission(), _require(), _require(), require_permissions(), _require(), _require() (+2 more)

### Community 24 - "test_notify_hooks.py"
Cohesion: 0.13
Nodes (8): StubWebSocket, test_admin_reply_notifies_owner(), test_admin_self_reply_stays_silent(), test_notifications_topic_format(), test_notify_persists_and_publishes(), test_permissions_update_notifies_admin(), test_priority_only_change_stays_silent(), test_status_change_notifies_owner()

### Community 25 - "Announcement"
Cohesion: 0.13
Nodes (9): Announcement, BroadcastEmail, build_broadcast_email(), _content_for(), _custom(), test_build_email_default_language_section_comes_first(), test_build_email_escapes_html_in_custom_content(), test_build_email_joins_every_language_title_in_subject() (+1 more)

### Community 26 - "list_my_tickets"
Cohesion: 0.09
Nodes (8): close_ticket(), create_ticket(), get_my_ticket(), list_my_tickets(), reply_ticket(), support_feed_ws(), authorize(), rate_limit_authenticated()

### Community 27 - "services/support_service.py"
Cohesion: 0.08
Nodes (29): SupportMessage, SupportMessageAttachment, SupportTicket, add_message(), attach_files(), count_unread(), count_unread_by_tickets(), create_ticket() (+21 more)

### Community 28 - "notify.py"
Cohesion: 0.18
Nodes (6): notifications_topic(), NotificationEventType, NotificationRealtimeEvent, NotificationType, notify(), notify_many()

### Community 30 - "config.py"
Cohesion: 0.05
Nodes (23): encrypt_secret(), _fernet(), generate_recovery_codes(), generate_totp_secret(), provisioning_uri(), verify_totp(), _explicit_secret_key(), _settings() (+15 more)

### Community 31 - "Notification"
Cohesion: 0.24
Nodes (7): Notification, count_unread(), create_notification(), get_notification(), list_notifications(), mark_all_read(), mark_read()

### Community 32 - "get_redis"
Cohesion: 0.18
Nodes (7): publish(), get_redis(), delete_root_transfer_otp(), _hash_code(), _key(), store_root_transfer_otp(), verify_root_transfer_otp()

### Community 33 - "list_broadcasts"
Cohesion: 0.15
Nodes (3): create_broadcast(), get_broadcast_templates(), list_broadcasts()

### Community 34 - "Language"
Cohesion: 0.14
Nodes (11): _format_datetime(), render_template(), Language, test_format_datetime_passthrough_on_invalid(), test_format_datetime_renders_utc_label(), test_render_template_formats_datetime_variables(), test_render_template_keeps_unknown_placeholder_intact(), test_render_template_picks_text_variable_for_language() (+3 more)

### Community 35 - "lifespan.py"
Cohesion: 0.08
Nodes (13): close_arq_pool(), get_arq_pool(), init_arq_pool(), lifespan(), _listen(), start_realtime(), stop_realtime(), _build_pool() (+5 more)

### Community 36 - "serve_account_socket"
Cohesion: 0.11
Nodes (7): account_events_ws(), _handle_command(), serve_account_socket(), serve_multiplex(), _serving(), test_frame_racing_the_close_ends_the_socket_quietly(), test_runtime_error_on_an_open_socket_still_surfaces()

### Community 37 - "is_login_locked"
Cohesion: 0.13
Nodes (10): clear_login_attempts(), _fail_key(), _hash(), is_login_locked(), _lock_key(), register_failed_login(), _lock_account(), test_authenticate_locks_and_emails() (+2 more)

### Community 38 - "broadcast_templates.py"
Cohesion: 0.16
Nodes (6): get_template(), list_templates(), RenderedContent, template_exists(), BroadcastTemplate, test_template_helpers_agree_on_existence()

### Community 39 - "broadcast_service.py"
Cohesion: 0.13
Nodes (12): list_announcements(), AnnouncementContent, AnnouncementCreator, AnnouncementKind, AnnouncementListResponse, AnnouncementRead, BroadcastCreate, BroadcastCreateResponse (+4 more)

### Community 40 - "notifications.py"
Cohesion: 0.09
Nodes (15): get_unread_count(), list_my_notifications(), mark_all_notifications_read(), mark_notification_read(), notifications_ws(), NotificationListResponse, NotificationRead, NotificationReadResponse (+7 more)

### Community 41 - "_account"
Cohesion: 0.16
Nodes (7): _account(), _role_id(), _role_keys(), test_account_keeps_a_user_role(), test_admin_assignment_needs_admins_write(), test_assignment_payload_is_checked(), test_expired_role_is_not_a_source()

### Community 42 - "_role_payload"
Cohesion: 0.10
Nodes (11): _role_payload(), _set_payload(), _store_role_assignment(), test_assigned_role_cannot_be_deleted(), test_audience_and_key_cannot_be_edited(), test_connected_account_sees_a_set_edit_at_once(), test_crud_routes_refuse_without_their_permission(), test_element_edits_and_deletes_take_the_lock() (+3 more)

### Community 43 - "_assign_set"
Cohesion: 0.18
Nodes (7): _assign_role(), _assign_set(), test_effective_is_union_of_roles_sets_and_direct_grants(), test_expired_assignment_stops_counting_without_invalidation(), test_future_expiry_and_no_expiry_both_count(), test_next_assignment_expiry_ignores_lapsed_and_unlimited_rows(), test_other_accounts_sources_do_not_leak()

### Community 44 - "env.py"
Cohesion: 0.20
Nodes (4): do_run_migrations(), run_async_migrations(), run_migrations_offline(), run_migrations_online()

### Community 45 - "user_mfa.py"
Cohesion: 0.14
Nodes (10): consume_recovery_code(), count_unused_recovery_codes(), delete_mfa(), enable_mfa(), get_mfa(), replace_recovery_codes(), update_last_used_step(), upsert_pending_mfa() (+2 more)

### Community 46 - "list_tickets"
Cohesion: 0.10
Nodes (7): admin_feed_ws(), authorize(), get_ticket(), list_tickets(), reply_ticket(), update_ticket(), permission_watcher()

### Community 47 - "get_stats"
Cohesion: 0.18
Nodes (4): get_stats(), get_admin_stats(), AdminStats, get_admin_stats_service()

### Community 48 - "sqlalchemy"
Cohesion: 0.03
Nodes (48): upgrade(), upgrade(), downgrade(), upgrade(), upgrade(), downgrade(), upgrade(), upgrade() (+40 more)

### Community 49 - "auth_service.py"
Cohesion: 0.05
Nodes (40): send_email(), admin_mfa_required(), averify_password(), decode_token_payload(), verify_new_account_token(), verify_password_reset_token(), UserSession, add_token_to_blacklist() (+32 more)

### Community 50 - "test_rbac_bootstrap.py"
Cohesion: 0.04
Nodes (29): ensure_system_rbac_catalog(), RbacRolePermissionSet, ensure_rbac_catalog(), test_account_topic_format(), test_patch_repairs_a_corrupt_stored_value(), create_test_database(), _enable_sqlite_foreign_keys(), override_get_db() (+21 more)

### Community 51 - "repositories/user.py"
Cohesion: 0.05
Nodes (21): downgrade(), scrub_details(), _scrubbed(), upgrade(), create_announcement(), deactivate_other_banners(), get_announcement(), _apply_audience() (+13 more)

### Community 52 - "announcements.py"
Cohesion: 0.21
Nodes (4): get_active_announcement(), get_active_banner(), ActiveBannerResponse, get_active_banner_service()

### Community 54 - "get_current_user"
Cohesion: 0.14
Nodes (11): _ensure_admin_mfa(), get_current_active_user(), get_current_admin_user(), get_current_session_id(), get_current_superadmin(), get_current_user(), get_ws_admin_user(), _has_required_mfa() (+3 more)

### Community 55 - "StubSocket"
Cohesion: 0.15
Nodes (4): StubSocket, test_watch_socket_rechecks_on_its_own_until_refused(), check(), test_watch_socket_separates_not_knowing_from_a_refusal()

### Community 56 - "routes/health.py"
Cohesion: 0.23
Nodes (8): _check_database(), _check_redis(), _elapsed_ms(), liveness(), readiness(), CheckResult, LivenessResponse, ReadinessResponse

### Community 57 - "storage.py"
Cohesion: 0.07
Nodes (12): _configure(), delete_file(), is_configured(), upload_file(), UploadResult, client(), disable_admin_mfa(), fake_redis() (+4 more)

### Community 58 - "test_redis_failure_falls_back_to_database_and_never_grants"
Cohesion: 0.13
Nodes (4): _BrokenRedis, test_invalidation_tolerates_redis_failure(), test_redis_failure_falls_back_to_database_and_never_grants(), test_uninitialized_redis_falls_back_to_database()

### Community 59 - "API Exception Handlers"
Cohesion: 0.16
Nodes (5): general_exception_handler(), http_exception_handler(), rate_limit_exception_handler(), register_exception_handlers(), validation_exception_handler()

### Community 61 - "watch_socket"
Cohesion: 0.18
Nodes (3): _wait_for_refusal(), _WakeOnFrame, watch_socket()

### Community 63 - "test_realtime.py"
Cohesion: 0.06
Nodes (20): get_ws_user(), ConnectionManager, create_access_token(), _allow(), _deny(), _seed_user(), StubWebSocket, test_can_user_access_ticket_gate() (+12 more)

### Community 64 - "Admin File Tests"
Cohesion: 0.21
Nodes (7): test_admin_delete_file_clears_avatar(), test_admin_files_requires_superuser(), test_admin_get_file_detail(), test_admin_list_files(), test_admin_list_files_filter_content_type(), test_admin_list_files_filter_uploader(), _upload()

### Community 65 - "SystemRole"
Cohesion: 0.13
Nodes (13): SystemRole, _make_user(), test_database_failure_is_not_swallowed(), test_generation_outlives_every_entry_and_then_expires(), test_invalidation_targets_a_single_account(), test_redis_write_failure_still_returns_the_database_answer(), test_require_any_permission_exposes_the_tuple_and_needs_one_key(), test_require_user_permission_accepts_regular_user_holding_the_key() (+5 more)

### Community 66 - "ActiveUser"
Cohesion: 0.09
Nodes (5): ActiveUser, _credentials(), HealthCeilingUser, _login(), LoginStormUser

### Community 67 - "register_and_verify"
Cohesion: 0.02
Nodes (93): admin_client(), get_user_id(), grant_all_permissions(), grant_permissions(), login(), nonroot_superadmin_client(), promote_to_admin(), promote_to_superadmin() (+85 more)

### Community 68 - "use_cases/settings.py"
Cohesion: 0.11
Nodes (12): coerce(), get_definition(), SettingCategory, SettingDefinition, SettingValueType, _validate_locale(), _validate_non_empty(), _validate_upload_size() (+4 more)

### Community 69 - "test_metrics.py"
Cohesion: 0.19
Nodes (5): root_client(), test_metrics_200_with_correct_token(), test_metrics_404_with_wrong_token(), test_metrics_404_without_token_in_production(), test_metrics_open_in_local()

### Community 70 - "make_user_client"
Cohesion: 0.14
Nodes (11): get_user_id(), seed_notification(), test_list_empty(), test_list_newest_first_and_unread_count(), test_list_only_my_notifications(), test_list_pagination_and_unread_only(), test_list_requires_auth(), test_mark_all_read() (+3 more)

### Community 71 - "_grant"
Cohesion: 0.13
Nodes (8): _grant(), _has(), test_account_without_any_source_has_nothing(), test_admin_permission_ignored_for_user_tier(), test_admin_tier_needs_the_key_in_its_effective_set(), test_expired_role_keeps_the_same_permission_from_another_source(), test_self_permission_works_for_user_tier(), test_users_me_lists_only_usable_keys_for_regular_user()

### Community 72 - "UserActivity"
Cohesion: 0.05
Nodes (32): actor_reference(), UserActivity, anonymize_user_activities(), anonymize_own_row(), strip_about_row(), create_user_activity(), purge_anonymized_activities(), _rewrite_in_batches() (+24 more)

### Community 74 - "system_settings_service.py"
Cohesion: 0.10
Nodes (16): to_str(), SystemSetting, get_all_system_settings(), get_system_setting_by_key(), upsert_system_setting(), PublicSettingsResponse, SettingRead, SettingsListResponse (+8 more)

### Community 75 - "test_rbac_route_coverage.py"
Cohesion: 0.09
Nodes (10): custom_generate_unique_id(), _app_routes(), _classification_problems(), _dependants(), _http_endpoints(), _is_superadmin_only(), _permissions(), test_admin_route_labelled_only_with_a_self_key_is_refused() (+2 more)

### Community 76 - "Origin Restriction Tests"
Cohesion: 0.32
Nodes (6): test_allowed_origin(), test_cross_origin_post_blocked(), test_no_origin(), test_same_origin_post(), test_same_origin_put(), test_unauthorized_origin()

### Community 77 - "user_topic"
Cohesion: 0.22
Nodes (4): _parse_ticket_topic(), user_topic(), test_parse_ticket_topic(), test_user_topic_format()

### Community 79 - "make_user_client"
Cohesion: 0.07
Nodes (30): TicketStatus, client_factory(), make_admin_client(), make_user_client(), open_ticket(), upload_png(), test_admin_cannot_reply_to_closed_ticket(), test_assign_to_non_admin_rejected() (+22 more)

### Community 80 - "rate_limit.py"
Cohesion: 0.09
Nodes (6): read_public_settings(), get_user_id(), rate_limit_public(), _storage_uri(), dummy_rate_limit_endpoint(), test_rate_limiter_exceed()

### Community 82 - "_find_kwarg"
Cohesion: 0.40
Nodes (3): decorator(), wrapper(), _find_kwarg()

### Community 83 - "mfa_service.py"
Cohesion: 0.10
Nodes (19): decrypt_secret(), hash_recovery_code(), MfaChallengeResponse, MfaEnrollConfirmResponse, MfaEnrollStartResponse, AuthTokens, _complete_login(), confirm_mfa_enrollment_service() (+11 more)

### Community 84 - "security.py"
Cohesion: 0.07
Nodes (24): _base_payload(), _create_email_token(), create_mfa_token(), create_password_reset_token(), create_refresh_token(), generate_new_account_token(), get_password_hash(), _verify_email_token() (+16 more)

### Community 85 - "repositories/rbac.py"
Cohesion: 0.08
Nodes (22): RbacPermissionSetItem, RbacUserPermissionSet, RbacUserRole, _apply_assignments(), assign_default_role(), get_account_ids_holding_role(), get_assigned_permissions(), get_permanent_assigned_permissions() (+14 more)

### Community 95 - "list_user_activities"
Cohesion: 0.14
Nodes (4): list_user_activities(), search_activities(), AdminActivityListResponse, list_user_activities_admin_service()

### Community 100 - "reset_mfa.py"
Cohesion: 0.17
Nodes (4): main(), run(), _run_and_dispose(), reset_user_mfa()

### Community 101 - "test_rbac_user_routes.py"
Cohesion: 0.04
Nodes (48): account_topic(), _admin_with_support_read(), AsgiSocket, _assign_only_role(), _hold_only(), _publish_permissions_updated(), _replace_with_expiring(), _seed_account() (+40 more)

### Community 102 - "log_activity"
Cohesion: 0.05
Nodes (25): require_permission(), SuccessMessages, reactivate_user(), AccountEvent, AccountEventType, ActivityStatus, ActivityType, ResourceType (+17 more)

### Community 113 - "test_rbac_api.py"
Cohesion: 0.10
Nodes (11): _last_audit(), _role_row(), test_assignment_reports_a_role_deleted_meanwhile(), test_assignments_are_audited_without_personal_data(), test_direct_grant_editor_demotes_on_the_last_grant(), test_element_lock_reads_fresh_rows_for_update(), test_promotion_does_not_revive_a_lingering_grant(), test_role_mutations_are_audited() (+3 more)

### Community 126 - "User"
Cohesion: 0.04
Nodes (50): confirm_transfer_root(), create_admin(), delete_admin(), demote_superadmin(), list_admins_endpoint(), list_permission_catalog(), promote_admin(), set_admin_permissions() (+42 more)

### Community 128 - "_make_user"
Cohesion: 0.12
Nodes (13): _cache_key(), _effective(), restore_redis(), test_already_expired_assignment_does_not_cap_the_ttl(), test_assignment_expiring_within_a_second_is_not_cached(), test_cache_ttl_is_capped_at_the_next_expiry(), test_cache_uses_the_configured_ttl_without_a_nearer_expiry(), test_corrupted_cache_entry_is_replaced_from_the_database() (+5 more)

### Community 166 - "services/user_service.py"
Cohesion: 0.10
Nodes (15): UserBase, UserCreate, UserMe, UserPublic, UsersPublic, UserUpdate, build_user_me_service(), _cleanup_old_avatar() (+7 more)

### Community 172 - "ErrorMessages"
Cohesion: 0.08
Nodes (22): ErrorMessages, _validate_password_strength(), _assert_refused(), test_access_of_a_user_hides_keys_outside_its_tier(), test_access_of_an_admin_needs_admins_read(), test_actor_cannot_change_its_own_access(), test_admin_target_needs_admins_write(), test_assignment_reports_a_set_deleted_meanwhile() (+14 more)

### Community 176 - "user_has_permission"
Cohesion: 0.17
Nodes (7): _root_client(), test_demotion_drops_a_cached_entry(), test_direct_grant_change_applies_immediately(), test_promotion_drops_the_cached_grants(), test_users_me_lists_nothing_for_account_without_role(), test_users_me_lists_self_permissions_for_regular_user(), test_users_me_still_omits_the_list_for_superadmin()

### Community 177 - "app/main.py"
Cohesion: 0.08
Nodes (6): get_db(), register_maintenance_middleware(), maintenance_mode_middleware(), init_metrics(), register_middleware(), init_sentry()

### Community 193 - "test_health.py"
Cohesion: 0.46
Nodes (4): test_liveness_returns_alive(), test_readiness_reports_database_failure(), test_readiness_returns_503_when_redis_unavailable(), test_readiness_returns_ready_when_dependencies_ok()

## Knowledge Gaps
- **88 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `tests/test_files.py`, `_make_user`, `User`, `admin/user_service.py`, `rbac_service.py`, `Permission`, `admin/support_service.py`, `Email Tokens and Success Messages`, `test_mfa_flow.py`, `test_rbac_effective.py`, `test_rbac.py`, `test_log_activity_defaults_success_status_code_to_200`, `test_scrub_audit_migration.py`, `admin/file_service.py`, `test_sessions.py`, `user_has_permission`, `services/support_service.py`, `_filtered_tickets_stmt`, `is_login_locked`, `services/user_service.py`, `broadcast_service.py`, `notifications.py`, `_assign_set`, `list_tickets`, `sqlalchemy`, `auth_service.py`, `test_rbac_bootstrap.py`, `repositories/user.py`, `get_current_user`, `test_realtime.py`, `SystemRole`, `register_and_verify`, `_grant`, `UserActivity`, `system_settings_service.py`, `mfa_service.py`, `security.py`, `repositories/rbac.py`, `test_rbac_user_routes.py`, `log_activity`, `test_rbac_api.py`?**
  _High betweenness centrality (0.151) - this node is a cross-community bridge._
- **Are the 43 inferred relationships involving `User` (e.g. with `_filtered_activities_stmt()` and `_filtered_files_stmt()`) actually correct?**
  _`User` has 43 INFERRED edges - model-reasoned connections that need verification._
- **Should `tests/test_files.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05261261261261261 - nodes in this community are weakly interconnected._
- **Why does `ErrorMessages` connect `ErrorMessages` to `admin/user_service.py`, `rbac_service.py`, `utc_now`, `Permission`, `admin/support_service.py`, `Email Tokens and Success Messages`, `test_mfa_flow.py`, `test_rbac.py`, `FileCategory`, `Broadcast Notification Tests`, `AsyncClient`, `auth.py`, `admin/file_service.py`, `test_sessions.py`, `test_maintenance_gate_blocks_admin_without_mfa_claim`, `services/support_service.py`, `services/user_service.py`, `broadcast_service.py`, `notifications.py`, `_account`, `_role_payload`, `app/main.py`, `auth_service.py`, `test_rbac_bootstrap.py`, `get_current_user`, `API Exception Handlers`, `register_and_verify`, `make_user_client`, `UserActivity`, `system_settings_service.py`, `make_user_client`, `mfa_service.py`, `security.py`, `list_user_activities`, `reset_mfa.py`, `test_rbac_user_routes.py`, `log_activity`, `test_rbac_api.py`, `User`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 126 inferred relationships involving `ErrorMessages` (e.g. with `register_maintenance_middleware()` and `refresh_token()`) actually correct?**
  _`ErrorMessages` has 126 INFERRED edges - model-reasoned connections that need verification._
- **Should `AsyncClient` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._
- **Why does `Permission` connect `Permission` to `_make_user`, `admin/user_service.py`, `rbac_service.py`, `admin/support_service.py`, `test_mfa_flow.py`, `test_rbac_effective.py`, `test_rbac.py`, `admin/file_service.py`, `test_set_admin_permissions_rejects_self_keys`, `test_permission_change_publishes_realtime_event`, `user_has_permission`, `test_sessions.py`, `services/support_service.py`, `services/user_service.py`, `broadcast_service.py`, `notifications.py`, `list_tickets`, `test_rbac_bootstrap.py`, `get_current_user`, `register_and_verify`, `_grant`, `system_settings_service.py`, `test_rbac_route_coverage.py`, `repositories/rbac.py`, `test_rbac_user_routes.py`, `log_activity`, `test_rbac_api.py`, `User`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._