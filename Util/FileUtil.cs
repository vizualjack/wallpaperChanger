using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WallpaperChanger.Util
{
    static class FileUtil
    {
        public static void SaveStringList(string filePath, List<string> dataList)
        {
            string content = "";
            foreach (string item in dataList) 
            {
                if (content.Length > 0) content += "\n";
                content += item;
            }
            File.WriteAllText(filePath, content);
        }
        public static List<string> ReadStringList(string filePath)
        {
            return File.ReadAllLines(filePath).ToList();
        }
        public static void SaveString(string filePath, string data) { File.WriteAllText(filePath, data); }
        public static string ReadString(string filePath) { return File.ReadAllText(filePath); }
        public static void SaveBytes(string filePath, byte[] data) { File.WriteAllBytes(filePath, data); }
        public static byte[] ReadBytes(string filePath) { return File.ReadAllBytes(filePath); }
    }
}
