using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.Serialization;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Animation;
using System.Windows.Media.Media3D;

namespace WallpaperChanger.Util
{
    class ExceptionSaver
    {
        public static ExceptionSaver instance = new ExceptionSaver(WallpaperChanger.Resources.EXCEPTION_FOLDER);

        string exceptionFolder;
        public ExceptionSaver(string exceptionFolder) 
        {
            this.exceptionFolder = exceptionFolder;
            if (!Directory.Exists(this.exceptionFolder))
                Directory.CreateDirectory(exceptionFolder);
        }

        public string saveException(Exception exception, string? addInfo) 
        {
            string exceptionInfo = exception.ToString();
            if (addInfo != null)
            {
                exceptionInfo += "=== Additional Info ===\n";
                exceptionInfo += addInfo;
            }
            string dateAsStr = DateTime.Now.ToString("yyyyMMddHHmmss");
            string logFileName = $"exception_{dateAsStr}.log";
            string logFilePath = Path.Combine(exceptionFolder, logFileName);
            FileUtil.SaveString(logFilePath, exceptionInfo);
            Logger.Error(exceptionInfo);
            return logFilePath;
        }
    }
}
