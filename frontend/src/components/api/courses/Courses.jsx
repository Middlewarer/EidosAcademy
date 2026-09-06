const BASE_URL = `${import.meta.env.VITE_API_URL}/api`;

export async function getCourses() {
    const response = await fetch(`${BASE_URL}/courses/`);
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.reason || "Не удалось загрузить курсы");
    }

    return data;
}







