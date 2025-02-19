﻿using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WallpaperChanger.Util
{
    public class Logger
    {
        public enum LogLevel { Debug, Info, Error}
        public static LogLevel logLevel = LogLevel.Info;

        public static void Debug(string message) { if(logLevel <= LogLevel.Debug) Print(LogLevel.Debug, message); }
        public static void Info(string message) { if (logLevel <= LogLevel.Info) Print(LogLevel.Info, message); }
        public static void Error(string message) { if (logLevel <= LogLevel.Error) Print(LogLevel.Error, message); }
        public static void Debug(object obj, string message) { if (logLevel <= LogLevel.Debug) Print(LogLevel.Debug, $"[{obj}] {message}"); }
        public static void Info(object obj, string message) { if (logLevel <= LogLevel.Info) Print(LogLevel.Info, $"[{obj}] {message}"); }
        public static void Error(object obj, string message) { if (logLevel <= LogLevel.Error) Print(LogLevel.Error, $"[{obj}] {message}"); }

        private static void Print(LogLevel logLevel, string message)
        {
            string formattedTimestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
            System.Diagnostics.Debug.WriteLine($"[{formattedTimestamp}] [{logLevel.ToString()}] {message}");
        }
    }
}
