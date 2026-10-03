export const LEGAL_VERSION = "02.10.2026";

export const legalConfig = {
  operatorName: import.meta.env.VITE_LEGAL_OPERATOR_NAME || "[УКАЖИТЕ ФИО ИЛИ НАИМЕНОВАНИЕ ОПЕРАТОРА]",
  operatorAddress: import.meta.env.VITE_LEGAL_OPERATOR_ADDRESS || "[УКАЖИТЕ АДРЕС ОПЕРАТОРА]",
  email: import.meta.env.VITE_LEGAL_EMAIL || "[УКАЖИТЕ EMAIL ДЛЯ ОБРАЩЕНИЙ]",
  siteUrl: import.meta.env.VITE_SITE_URL || "https://eidosacademy.ru",
  dataLocation: import.meta.env.VITE_LEGAL_DATA_LOCATION || "[УКАЖИТЕ МЕСТО НАХОЖДЕНИЯ БАЗЫ ДАННЫХ В РФ]",
};

export const hasCompleteLegalDetails = !Object.values(legalConfig).some((value) => value.startsWith("["));
