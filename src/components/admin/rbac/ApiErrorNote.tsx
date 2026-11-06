"use client";

import { CircleAlert } from "lucide-react";
import { useTranslation } from "react-i18next";

import { getApiErrorKey } from "@/lib/api/error-message";

interface ApiErrorNoteProps {
  error: unknown;
}

// The API refuses with a message key (system element, in use, audience mismatch,
// privilege escalation...). The global interceptor already toasts it; this keeps
// the reason on screen next to the form or dialog that caused it.
export function ApiErrorNote({ error }: ApiErrorNoteProps) {
  const { t } = useTranslation("errors");
  const key = getApiErrorKey(error);
  if (!error || !key) return null;
  return (
    <p
      role="alert"
      data-testid="rbac-api-error"
      className="mt-3 flex items-start gap-1.5 text-sm text-destructive"
    >
      <CircleAlert className="mt-0.5 h-4 w-4 shrink-0" />
      {t(key, { defaultValue: key })}
    </p>
  );
}
