import { apiRequest } from "../apiRequest";

export async function getCourses() {
    const response = await apiRequest("/api/courses/", { auth: false });
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.reason || "Не удалось загрузить курсы");
    }

    return data;
}







