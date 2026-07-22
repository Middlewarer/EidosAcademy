const BASE_URL = "http://127.0.0.1:8000/api"

export async function getCourses() {
    const response = await fetch(`${BASE_URL}/courses/`);
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.reason || "Не удалось загрузить курсы");
    }

    return data;
}







