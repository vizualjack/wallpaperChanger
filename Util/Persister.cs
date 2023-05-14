using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json.Nodes;
using System.Threading.Tasks;

namespace WallpaperChanger.Util
{
    class Persister
    {
        string persisterFile;
        JsonNode data;
        public Persister(string persisterFile)
        {
            this.persisterFile = persisterFile;
            data = new JsonObject();
            Load();
        }

        public void Load(Persistable persistable)
        {
            string? jsonString = GetData(GetClassName(persistable));
            if (jsonString == null) return;
            var jsonNode = JsonNode.Parse(jsonString);
            if(jsonNode == null) return;
            persistable.LoadFromJson(jsonNode);
        }

        public void AddForSave(Persistable persistable)
        {
            SetData(GetClassName(persistable), persistable.GetSaveData().ToJsonString());
        }

        public void Save()
        {
            FileUtil.SaveString(persisterFile, data.ToJsonString());
        }

        private string GetClassName(object obj) { return obj.GetType().Name; }

        private string? GetData(string key)
        {
            JsonNode? node = data[key];
            if (node == null) return null;
            return node.ToString();
        }

        private void SetData(string key, string value)
        {
            data[key] = value;
        }

        private void Load()
        {
            if (!File.Exists(persisterFile)) return;
            string jsonStr = File.ReadAllText(persisterFile);
            JsonNode? loadedJson = JsonObject.Parse(jsonStr);
            if (loadedJson != null) data = loadedJson;
        }
    }

    interface Persistable
    {
        public JsonNode GetSaveData();
        public void LoadFromJson(JsonNode jsonObject);
    }
}
