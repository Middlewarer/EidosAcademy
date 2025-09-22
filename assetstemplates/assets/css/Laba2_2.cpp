#include <Windows.h>
#include <iostream>
#include <iomanip>
using namespace std;

bool is_pressed(int vkey)
{
    // вернет истину, если указанная виртуальная клавиша 
    SHORT res = GetKeyState(vkey); // SHORT - целое 16 бит
    res = res & (1 << 15);  // зануляем все биты кроме 15 (старшего)
    return res != 0;
}

int main()
{
    SYSTEMTIME now;
    bool useLocalTime = true; 
    
    while (!is_pressed(VK_ESCAPE))
    {
        
        if (is_pressed(VK_SPACE))
        {
            useLocalTime = !useLocalTime; 
            
        }
        
        
        if (useLocalTime)
        {
            GetLocalTime(&now);
        }
        else
        {
            GetSystemTime(&now);
        }
        
        
        cout

            << setw(2) << setfill('0') << now.wHour << ":"
            << setw(2) << setfill('0') << now.wMinute << ":"
            << setw(2) << setfill('0') << now.wSecond
            << setw(8) << setfill('\x08') <<"";
            
        Sleep(100);
    }
    return 0;
}