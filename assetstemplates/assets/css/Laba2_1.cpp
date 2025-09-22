#include <Windows.h>>
int main() {
	HANDLE stdout = GetStdHandle(STD_OUTPUT_HANDLE);
	if (stdout == INVALID_HANDLE_VALUE)
		return 1;// проверяем программу
	// удалось - работаем...
	// указатель на неизменный символ - адрес первого символа строки
	// строка в кодировке ANSI. 1 символ - 1 байт.

	const char* messege = "Hello World!\n";// компилятор сам добавит завершающий \В
	DWORD len = strlen(messege);// длина строки в символах (= длине в байтах)
	DWORD written; // сколько байт реально бало записано
	BOOL success = WriteFile(
		stdout, // куда пишем
		messege, // адрес, где начинаются данные (что пишем)
		len, // длина данных в байтах
		&written,// не используется - передаем нулевой адрес
		NULL
	);
	if (!success || (len != written))// если запись не удалась или записали все
		return 2;
	return 0;
}