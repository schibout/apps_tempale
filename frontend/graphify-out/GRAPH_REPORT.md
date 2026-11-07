# Graph Report - frontend  (2026-11-07)

## Corpus Check
- 452 files · ~135,698 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 6, .example 1, .ico 1)

## Summary
- 1944 nodes · 7502 edges · 93 communities (78 shown, 15 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 22 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1cf2e707`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ActivityTable.tsx
- motion
- AdminUser
- TicketStatusBadge.tsx
- AuthButtons.tsx
- file.ts
- react
- ROUTES
- Playwright E2E Tests
- Localization Resources
- Admin Test Helpers
- UserAccessAssignModal.tsx
- BroadcastComposer.tsx
- Broadcast History and Dialogs
- UsersTable.tsx
- utils.ts
- Admin Permissions UI
- User and Settings Forms
- Runtime Dependencies
- useAuthStore
- PermissionSetsContent.tsx
- msw/server.ts
- CI Workflow
- file.ts
- Support API and Query Hooks
- ApiErrorNote.tsx
- types/admin.ts
- Development Tooling Dependencies
- MessageThread.tsx
- ROUTES
- [locale]/layout.tsx
- ESLint Configuration
- vitest
- AdminListItem
- types/rbac.ts
- Support Playwright Tests
- TypeScript Compiler Configuration
- types/notification.ts
- env.ts
- HeroFeedMock.tsx
- SupportContent.tsx
- Realtime Support Hooks
- RolesContent.test.tsx
- getLocalizedPath
- @tanstack/react-query
- NotificationsView.tsx
- metadata.ts
- next
- use-permissions.ts
- SystemSettingsContent.tsx
- Frontend Package Scripts
- support-socket.ts
- Notification Helpers and Tests
- Workspace and Package Overrides
- Local Storage Hook
- AntdProvider.tsx
- UserAccessPanel.test.tsx
- ClientSideProviders.tsx
- use-support.test.tsx
- MaintenanceGate.tsx
- PageTransition.tsx
- ErrorBoundaryBase
- TypeScript ESLint Configuration
- lucide-react
- AppDrawer.test.tsx
- Vite and Vitest Setup
- announcement-banner.spec.ts
- admin/(protected)/support/[id]/page.tsx
- [locale]/(protected)/layout.tsx
- Code Review Guidance
- PostCSS Configuration
- UI and API Architecture
- Hooks and i18n Architecture
- Realtime State Architecture
- Next.js Template Overview
- Utility and API Layer
- Zod Validation
- Playwright E2E Coverage
- package.json
- [locale]/(protected)/support/page.tsx
- renderWithProviders
- react-i18next
- EditPermissionsModal.test.tsx
- AdminSidebar.tsx
- schemas/support.ts
- HomeFooter.tsx
- proxy.ts
- api.ts
- [locale]/(protected)/support/[id]/page.tsx
- UsersFilters.tsx
- reset-password/page.tsx
- ProfileContent

## God Nodes (most connected - your core abstractions)
1. `Button()` - 128 edges
2. `react-i18next` - 121 edges
3. `getLocalizedPath()` - 100 edges
4. `Permission` - 95 edges
5. `cn()` - 92 edges
6. `react` - 90 edges
7. `ROUTES` - 84 edges
8. `next` - 82 edges
9. `useAuthStore` - 81 edges
10. `vitest` - 81 edges

## Surprising Connections (you probably didn't know these)
- `MockUser` --references--> `Permission`  [EXTRACTED]
  tests-e2e/account/deactivate.spec.ts → src/lib/types/permissions.ts
- `NotificationMockState` --references--> `NotificationItem`  [EXTRACTED]
  tests-e2e/notifications/notification-helpers.ts → src/lib/types/notification.ts
- `AssignModalProps` --references--> `UserAccess`  [EXTRACTED]
  src/components/admin/users/UserAccessAssignModal.tsx → src/lib/types/rbac.ts
- `UserAccessPanelProps` --references--> `AdminUser`  [EXTRACTED]
  src/components/admin/users/UserAccessPanel.tsx → src/lib/types/admin.ts
- `TicketStatusBadgeProps` --references--> `TicketStatus`  [EXTRACTED]
  src/components/support/TicketStatusBadge.tsx → src/lib/types/support.ts

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **RBAC & Permission System** — src_hooks_usepermissions, src_stores, src_lib_websocket, src_app_locale [EXTRACTED 1.00]
- **Automated Review Pipeline** — claude_commands_review, review_md, tests_e2e [INFERRED 0.90]

## Communities (93 total, 15 thin omitted)

### Community 0 - "ActivityTable.tsx"
Cohesion: 0.16
Nodes (16): ActivityDetails(), ActivityTable(), ActivityTableProps, actorLabel(), formatScalar(), isScalar(), ScalarJson, statusCodeTone() (+8 more)

### Community 1 - "motion"
Cohesion: 0.15
Nodes (19): HomeContent(), Home(), SectionHeader(), HomeFeatures(), HomeHero(), HomeMarquee(), MarqueeRow(), MarqueeRowProps (+11 more)

### Community 2 - "AdminUser"
Cohesion: 0.22
Nodes (15): Pending, AdminTierCaps, canMutateTarget(), capsForTarget(), NO_ADMIN_TIER_CAPS, UserActionCaps, caps, UserActionDialogsProps (+7 more)

### Community 3 - "TicketStatusBadge.tsx"
Cohesion: 0.18
Nodes (12): SupportTicketsTableProps, TicketList(), TicketListProps, PRIORITY_TONE, STATUS_TONE, TicketPriorityBadge(), TicketPriorityBadgeProps, TicketStatusBadge() (+4 more)

### Community 4 - "AuthButtons.tsx"
Cohesion: 0.12
Nodes (35): AdminSidebarFooter(), AdminSidebarFooterProps, AuthButtons(), AuthButtonsProps, MENU_ENTRIES, MenuEntry, drawerItem, drawerList (+27 more)

### Community 5 - "file.ts"
Cohesion: 0.11
Nodes (16): FilesTableProps, imageRow, orphanRow, mockFile, avatar, currentUser, file, mockAdminFile (+8 more)

### Community 6 - "react"
Cohesion: 0.09
Nodes (29): react, PermissionSetFormBody(), RoleFormBody(), GlobalError(), ELEMENT_KEY_PATTERN, ErrorBoundaryProps, ErrorBoundaryState, ErrorPage() (+21 more)

### Community 7 - "ROUTES"
Cohesion: 0.10
Nodes (29): generateMetadata(), AdminLoginPage(), generateMetadata(), generateMetadata(), AdminAdminsPage(), generateMetadata(), generateMetadata(), generateMetadata() (+21 more)

### Community 8 - "Playwright E2E Tests"
Cohesion: 0.16
Nodes (12): @playwright/test, baseUser, test, avatarFile, baseUser, PNG_BUFFER, mockUser, getStrings() (+4 more)

### Community 9 - "Localization Resources"
Cohesion: 0.09
Nodes (6): resources, LANGUAGES, Locale, Namespace, resources, bundles

### Community 10 - "Admin Test Helpers"
Cohesion: 0.10
Nodes (31): badLogin, baseActivity, ADMIN_PERMISSIONS, adminFile, adminListItems, adminUser, ALL_PERMISSIONS, injectSession() (+23 more)

### Community 11 - "UserAccessAssignModal.tsx"
Cohesion: 0.13
Nodes (25): EditPermissionsBody(), EditPermissionsModal(), TierWarning(), TierWarningProps, AssignBody(), AssignKind, AssignModalProps, AssignOption (+17 more)

### Community 12 - "BroadcastComposer.tsx"
Cohesion: 0.05
Nodes (71): i18next, BroadcastsContent(), AdminBroadcastsPage(), AnnouncementPreview(), AnnouncementPreviewProps, LEVEL_ACCENT, BroadcastComposer(), buildVariables() (+63 more)

### Community 13 - "Broadcast History and Dialogs"
Cohesion: 0.12
Nodes (24): ConfirmDialog(), ConfirmDialogProps, UserAvatarCard(), DeviceIcon(), DeviceIconProps, MOBILE_OS, SessionRow(), SessionRowProps (+16 more)

### Community 14 - "UsersTable.tsx"
Cohesion: 0.31
Nodes (20): AdminsTable(), FilesTable(), fullName(), isImage(), AdminTable(), AdminTableStateRow(), AdminTableStateRowProps, AdminTbody() (+12 more)

### Community 15 - "utils.ts"
Cohesion: 0.10
Nodes (29): motion, AboutContent(), ValueDef, VALUES, About(), SectionHeaderProps, TiltCard(), TiltCardProps (+21 more)

### Community 16 - "Admin Permissions UI"
Cohesion: 0.06
Nodes (36): PermissionGateProps, PermissionsApi, Permission, ActivitiesRead, AdminsDelete, AdminsRead, AdminsWrite, BroadcastRead (+28 more)

### Community 17 - "User and Settings Forms"
Cohesion: 0.12
Nodes (42): AdminRow(), StatCard(), AccountDeactivatedContent(), AccountDeactivatedPage(), AccountSuspendedContent(), ProfileContentProps, ProfileTab, TabDef (+34 more)

### Community 18 - "Runtime Dependencies"
Cohesion: 0.07
Nodes (30): dependencies, @ant-design/cssinjs@^2.1.2, @ant-design/icons@^6.2.5, @ant-design/nextjs-registry@^1.3.0, antd@^6.4.3, axios@^1.17.0, clsx@^2.1.1, i18next@^25.10.10 (+22 more)

### Community 19 - "useAuthStore"
Cohesion: 0.07
Nodes (27): ticket, detail, allCaps, baseUser, renderZone(), UpdateUserParams, userKeys, usersApi (+19 more)

### Community 20 - "PermissionSetsContent.tsx"
Cohesion: 0.16
Nodes (22): AdminForbidden(), AdminPermissionSetsPage(), PermissionSetFormModal(), PermissionSetsContent(), AdminRolesPage(), RoleFormModal(), RolesContent(), AudienceBadge() (+14 more)

### Community 21 - "msw/server.ts"
Cohesion: 0.15
Nodes (15): msw, mockPush, avatar, userWithAvatar, mockReplace, PageContent(), renderHydrator(), mockLoginResponse() (+7 more)

### Community 22 - "CI Workflow"
Cohesion: 0.08
Nodes (24): concurrency, cancel-in-progress, group, jobs, lint-and-typecheck, name, runs-on, steps (+16 more)

### Community 23 - "file.ts"
Cohesion: 0.16
Nodes (21): AvatarActions(), AvatarActionsProps, AvatarUpload(), AvatarUploadProps, DEFAULT_IMAGE_TYPES, DEFAULT_MAX_UPLOAD_SIZE, FileValidationError, formatBytes() (+13 more)

### Community 24 - "Support API and Query Hooks"
Cohesion: 0.15
Nodes (22): TicketAdminControlsProps, ReplyBoxProps, invalidateAdminSurfaces(), QueryClient, useAdminReplyTicket(), adminSupportApi, userSupportApi, AdminTicketDetail (+14 more)

### Community 25 - "ApiErrorNote.tsx"
Cohesion: 0.24
Nodes (7): ApiErrorNote(), ApiErrorNoteProps, RbacDeleteDialog(), RbacDeleteDialogProps, ErrorBody, getApiErrorKey(), getApiErrorStatus()

### Community 26 - "types/admin.ts"
Cohesion: 0.06
Nodes (64): ActivitiesContent(), ACTIVITY_TYPES, isResourceFilter(), isStatusFilter(), isTypeFilter(), parseStatusCodeFilter(), RESOURCE_TYPES, ResourceFilter (+56 more)

### Community 27 - "Development Tooling Dependencies"
Cohesion: 0.09
Nodes (22): devDependencies, eslint-config-next@16.1.6, eslint-import-resolver-typescript@^4.4.5, husky@^9.1.7, jsdom@^29.1.1, msw@^2.14.6, @playwright/test@^1.60.0, prettier@^3.8.3 (+14 more)

### Community 28 - "MessageThread.tsx"
Cohesion: 0.43
Nodes (5): AttachmentThumb(), AttachmentThumbProps, MessageThreadProps, SenderRole, SupportMessage

### Community 29 - "ROUTES"
Cohesion: 0.38
Nodes (6): AdminActivitiesPage(), AdminFilesPage(), PermissionGate(), AdminSupportPage(), AdminUsersPage(), ROUTES

### Community 30 - "[locale]/layout.tsx"
Cohesion: 0.25
Nodes (6): albertSans, fraunces, geistMono, generateMetadata(), RootLayout(), THEME_STYLES

### Community 31 - "ESLint Configuration"
Cohesion: 0.10
Nodes (20): eslint@^9.39.4, eslint-config-prettier@^10.1.8, @eslint/js@^10.0.1, eslint-plugin-import@^2.32.0, eslint-plugin-jsx-a11y@^6.10.2, eslint-plugin-react@^7.37.5, eslint-plugin-react-hooks@^7.1.1, eslint-plugin-react-refresh@^0.5.2 (+12 more)

### Community 32 - "vitest"
Cohesion: 0.14
Nodes (16): @testing-library/react, vitest, mockSearchParams, user, renderModal(), ticketResponse, setup(), mockNotification (+8 more)

### Community 33 - "AdminListItem"
Cohesion: 0.24
Nodes (10): buildRowMenu(), RowMenuActions, RowMenuArgs, AdminRowProps, AdminsTableProps, EditPermissionsBodyProps, EditPermissionsModalProps, menuKeys() (+2 more)

### Community 34 - "types/rbac.ts"
Cohesion: 0.15
Nodes (22): BodyProps, PermissionSetFormModalProps, RoleFormBodyProps, RoleFormModalProps, QueryClient, rbacApi, AssignmentsUpdatePayload, EffectivePermission (+14 more)

### Community 35 - "Support Playwright Tests"
Cohesion: 0.18
Nodes (18): adminMessage, adminTicketDetail, adminTicketListItem, closedAdminTicketDetail, closedTicketDetail, listResponse(), mockAdminReply(), mockAdminTicketDetail() (+10 more)

### Community 36 - "TypeScript Compiler Configuration"
Cohesion: 0.11
Nodes (18): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+10 more)

### Community 37 - "types/notification.ts"
Cohesion: 0.18
Nodes (9): JsonValue, NotificationRealtimeEvent, createNotificationSocket(), connect(), NotificationSocket, FakeWebSocket, jsonValueSchema, notificationItemSchema (+1 more)

### Community 38 - "env.ts"
Cohesion: 0.11
Nodes (17): nextConfig, securityHeaders, @sentry/nextjs, generateMetadata(), viewport, alt, contentType, Image() (+9 more)

### Community 39 - "HeroFeedMock.tsx"
Cohesion: 0.29
Nodes (7): advanceFeed(), FEED_POOL, FeedEntry, HeroFeedMock(), HeroFeedMockProps, MockAuthor, SPRING_SOFT

### Community 40 - "SupportContent.tsx"
Cohesion: 0.13
Nodes (27): FilesContent(), AdminSupportContent(), StatusFilter, SupportContent(), FILE_CONTENT_TYPES, FilesFilters(), FilesFiltersProps, AdminPagination() (+19 more)

### Community 41 - "Realtime Support Hooks"
Cohesion: 0.21
Nodes (11): adminSupportKeys, supportKeys, SupportSocket, appendMessage(), ConnectArgs, SupportRealtimeState, useSupportRealtimeStore, connect() (+3 more)

### Community 42 - "RolesContent.test.tsx"
Cohesion: 0.22
Nodes (6): adminSet, customRole, stamp, systemRole, userSet, WRITER

### Community 43 - "getLocalizedPath"
Cohesion: 0.06
Nodes (89): antd, axios, zod, AdminLoginContent(), CreateAdminModal(), CreateAdminModalProps, groupByResource(), PermissionGroup (+81 more)

### Community 44 - "@tanstack/react-query"
Cohesion: 0.43
Nodes (4): @tanstack/react-query, getQueryClient(), queryDefaults, QueryProvider()

### Community 45 - "NotificationsView.tsx"
Cohesion: 0.11
Nodes (34): AdminNotificationsContent(), AdminNotificationsPage(), InboxRow(), InboxRowProps, notificationTargetPath(), notificationText(), readNotificationString(), NotificationBell() (+26 more)

### Community 46 - "metadata.ts"
Cohesion: 0.16
Nodes (11): AdminDashboardPage(), generateMetadata(), ForgotPassword(), generateMetadata(), resolvePageMeta(), seoTranslations, BuildMetadataOptions, SeoLocale (+3 more)

### Community 47 - "next"
Cohesion: 0.12
Nodes (11): next, AdminIndexPage(), AdminIndexPageProps, AdminProtectedLayout(), AdminProtectedLayoutProps, AdminUserDetailPage(), generateMetadata(), UserDetailPageProps (+3 more)

### Community 48 - "use-permissions.ts"
Cohesion: 0.17
Nodes (25): AdminsContent(), TransferRootModal(), UserDetailContent(), UsersContent(), UserActionDialogs(), useAdmins(), useAdminUser(), useConfirmTransferRoot() (+17 more)

### Community 49 - "SystemSettingsContent.tsx"
Cohesion: 0.18
Nodes (16): AdminSystemSettingsPage(), SystemSettingsContent(), SystemSettingsFormProps, systemSettingsKeys, useSystemSettings(), useUpdateSystemSetting(), useCanWriteSystemSettings(), systemSettingsApi (+8 more)

### Community 50 - "Frontend Package Scripts"
Cohesion: 0.18
Nodes (11): scripts, build, dev, format, format:check, lint, prepare, start (+3 more)

### Community 51 - "support-socket.ts"
Cohesion: 0.17
Nodes (12): RealtimeEvent, AccountSocket, createAccountSocket(), connect(), buildWsUrl(), createReconnectingSocket(), connect(), SocketOptions (+4 more)

### Community 52 - "Notification Helpers and Tests"
Cohesion: 0.36
Nodes (7): bellBadge(), fillTemplate(), mockNotifications(), permissionsNotification, repliedNotification, unreadCount(), WebSocketRoute

### Community 53 - "Workspace and Package Overrides"
Cohesion: 0.20
Nodes (9): allowBuilds, msw, @sentry/cli, sharp, unrs-resolver, overrides, postcss, vite (+1 more)

### Community 55 - "AntdProvider.tsx"
Cohesion: 0.17
Nodes (14): buildThemeStyleSheet(), camelToKebab(), colorsToCssDeclarations(), darkAntdTokens, darkColors, lightAntdTokens, lightColors, ThemeColors (+6 more)

### Community 56 - "UserAccessPanel.test.tsx"
Cohesion: 0.29
Nodes (5): access, baseUser, FULL, memberRole, roleOptions

### Community 57 - "ClientSideProviders.tsx"
Cohesion: 0.27
Nodes (7): ErrorBoundary(), ClientSideProviders(), ClientSideProvidersProps, loadingMessages, mockChangeLanguage, mockedI18n, ThemeProvider()

### Community 58 - "use-support.test.tsx"
Cohesion: 0.29
Nodes (4): listItem, mockAdminTicketDetail, mockMessage, mockTicketDetail

### Community 59 - "MaintenanceGate.tsx"
Cohesion: 0.47
Nodes (4): MaintenanceGate(), MaintenanceGateProps, MaintenanceScreen(), authRoutes

### Community 60 - "PageTransition.tsx"
Cohesion: 0.60
Nodes (3): Template(), PageTransition(), PageTransitionProps

### Community 62 - "TypeScript ESLint Configuration"
Cohesion: 0.40
Nodes (4): ./tsconfig.json, exclude, extends, include

### Community 63 - "lucide-react"
Cohesion: 0.13
Nodes (27): lucide-react, AdminTicketDetailContent(), AdminTicketDetailContentProps, NotificationsContent(), TicketDetailContent(), TicketDetailContentProps, PermissionNote(), PermissionNoteProps (+19 more)

### Community 64 - "AppDrawer.test.tsx"
Cohesion: 0.40
Nodes (4): createMockUser(), defaultProps, mockAuthenticated(), mockPush

### Community 66 - "announcement-banner.spec.ts"
Cohesion: 0.40
Nodes (3): activeBanner, DISMISS, TITLE

### Community 67 - "admin/(protected)/support/[id]/page.tsx"
Cohesion: 0.50
Nodes (3): AdminTicketPage(), AdminTicketPageProps, generateMetadata()

### Community 68 - "[locale]/(protected)/layout.tsx"
Cohesion: 0.39
Nodes (5): ProtectedLayout(), ProtectedLayoutProps, AccountEventsBridge(), sessionKeys, useAccountEvents()

### Community 79 - "package.json"
Cohesion: 0.11
Nodes (17): lint-staged@^16.4.0, @tailwindcss/postcss@^4.3.0, @testing-library/dom@^10.4.1, @testing-library/jest-dom@^6.9.1, @types/react@^19.2.17, @types/react-dom@^19.2.3, typescript@^5.9.3, name (+9 more)

### Community 81 - "renderWithProviders"
Cohesion: 0.11
Nodes (15): @testing-library/user-event, mockChangePassword, mockDeactivate, mockReactivate, mockUpdateMe, mockUser, logo, renderForm() (+7 more)

### Community 83 - "react-i18next"
Cohesion: 0.15
Nodes (21): react-i18next, AdminShell(), AdminShellProps, AdminTopbar(), AdminTopbarProps, DashboardContent(), Logout(), VerifyEmailContent() (+13 more)

### Community 84 - "EditPermissionsModal.test.tsx"
Cohesion: 0.17
Nodes (10): accessWith(), admin, adminRole, mockAccess(), renderModal(), ALL, catalog, stamp (+2 more)

### Community 85 - "AdminSidebar.tsx"
Cohesion: 0.21
Nodes (12): AdminNavCaps, AdminNavItem, AdminNavSection, buildAdminNav(), AdminSidebar(), AdminSidebarProps, itemKeys(), noCaps (+4 more)

### Community 86 - "schemas/support.ts"
Cohesion: 0.22
Nodes (8): adminTicketListItemSchema, CreateTicketFormValues, fileCategorySchema, filePublicSchema, realtimeEventSchema, ReplyFormValues, supportMessageSchema, supportTicketUserSchema

### Community 87 - "HomeFooter.tsx"
Cohesion: 0.20
Nodes (12): next-themes@^0.4.6, next-themes, BackToTop(), FooterColumn(), FooterColumnProps, FooterLink, HomeFooter(), LOCALES (+4 more)

### Community 89 - "proxy.ts"
Cohesion: 0.17
Nodes (14): Locale-based Routing, usePermissions Hook, adminRoutes, defaultLocale, Locale, locales, protectedRoutes, publicAuthRoutes (+6 more)

### Community 90 - "api.ts"
Cohesion: 0.15
Nodes (24): adminRedirectTarget(), AuthHydrator(), AppHeader(), HeaderNav(), HeaderNavLink, HeaderNavProps, LANGUAGE_OPTIONS, LanguageMenu() (+16 more)

### Community 91 - "[locale]/(protected)/support/[id]/page.tsx"
Cohesion: 0.50
Nodes (3): generateMetadata(), SupportTicketPage(), SupportTicketPageProps

### Community 92 - "UsersFilters.tsx"
Cohesion: 0.26
Nodes (11): isUsersRoleFilter(), isUsersStatusFilter(), isUsersVerifiedFilter(), USERS_ROLE_FILTERS, USERS_STATUS_FILTERS, USERS_VERIFIED_FILTERS, UsersRoleFilter, UsersStatusFilter (+3 more)

### Community 96 - "ProfileContent"
Cohesion: 0.38
Nodes (5): AdminProfile(), generateMetadata(), generateMetadata(), Profile(), ProfileContent()

## Knowledge Gaps
- **50 isolated node(s):** `ActivitiesRead`, `AdminsDelete`, `AdminsRead`, `AdminsWrite`, `BroadcastRead` (+45 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 518 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `react-i18next` connect `react-i18next` to `ActivityTable.tsx`, `motion`, `AdminUser`, `TicketStatusBadge.tsx`, `AuthButtons.tsx`, `react`, `Localization Resources`, `UserAccessAssignModal.tsx`, `BroadcastComposer.tsx`, `Broadcast History and Dialogs`, `UsersTable.tsx`, `utils.ts`, `User and Settings Forms`, `Runtime Dependencies`, `PermissionSetsContent.tsx`, `file.ts`, `ApiErrorNote.tsx`, `types/admin.ts`, `MessageThread.tsx`, `HeroFeedMock.tsx`, `SupportContent.tsx`, `getLocalizedPath`, `NotificationsView.tsx`, `use-permissions.ts`, `SystemSettingsContent.tsx`, `MaintenanceGate.tsx`, `lucide-react`, `package.json`, `AdminSidebar.tsx`, `HomeFooter.tsx`, `api.ts`, `UsersFilters.tsx`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **What connects `ActivitiesRead`, `AdminsDelete`, `AdminsRead` to the rest of the system?**
  _50 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `motion` be split into smaller, more focused modules?**
  _Cohesion score 0.14855072463768115 - nodes in this community are weakly interconnected._
- **Why does `vitest` connect `vitest` to `ActivityTable.tsx`, `AdminUser`, `TicketStatusBadge.tsx`, `AuthButtons.tsx`, `file.ts`, `BroadcastComposer.tsx`, `useAuthStore`, `PermissionSetsContent.tsx`, `msw/server.ts`, `file.ts`, `ApiErrorNote.tsx`, `types/admin.ts`, `Development Tooling Dependencies`, `AdminListItem`, `types/notification.ts`, `Realtime Support Hooks`, `RolesContent.test.tsx`, `getLocalizedPath`, `@tanstack/react-query`, `use-permissions.ts`, `support-socket.ts`, `Local Storage Hook`, `UserAccessPanel.test.tsx`, `ClientSideProviders.tsx`, `use-support.test.tsx`, `AppDrawer.test.tsx`, `Vite and Vitest Setup`, `package.json`, `renderWithProviders`, `EditPermissionsModal.test.tsx`, `AdminSidebar.tsx`, `HomeFooter.tsx`, `UsersFilters.tsx`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Should `AuthButtons.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.11738648947951273 - nodes in this community are weakly interconnected._
- **Why does `Permission` connect `Admin Permissions UI` to `file.ts`, `react`, `Playwright E2E Tests`, `Admin Test Helpers`, `UserAccessAssignModal.tsx`, `useAuthStore`, `msw/server.ts`, `types/admin.ts`, `ROUTES`, `vitest`, `AdminListItem`, `types/rbac.ts`, `Support Playwright Tests`, `SupportContent.tsx`, `RolesContent.test.tsx`, `getLocalizedPath`, `use-permissions.ts`, `UserAccessPanel.test.tsx`, `use-support.test.tsx`, `lucide-react`, `renderWithProviders`, `EditPermissionsModal.test.tsx`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Should `file.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.11396011396011396 - nodes in this community are weakly interconnected._