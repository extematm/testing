using System;
using System.Data.SqlClient;

class Program
{
    static void Main()
    {
        string userInput = Console.ReadLine();
        string query = "SELECT * FROM Users WHERE name = '" + userInput + "'";
        SqlCommand cmd = new SqlCommand(query);
        var md5 = System.Security.Cryptography.MD5.Create();
    }
}