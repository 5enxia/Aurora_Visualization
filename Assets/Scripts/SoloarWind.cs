using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System.IO;

// SolarWind
    public class SolarWind
    {
        public string time;
        public float density;
        public float speed;
        public int tempareture;


        public static SolarWind load(string fn)
        {
            string jsonFilePath = fn;
            string data = File.ReadAllText(jsonFilePath);
            return JsonUtility.FromJson<SolarWind>(data);
        }

        public void save(string fn)
        {
            string text = JsonUtility.ToJson(this, true);
            File.WriteAllText(fn, text);
        }

        void printParams()
        {
            Debug.Log(this);
        }

        public SolarWind()
        {

        }

        public SolarWind(string time, float density, float speed, int tempareture)
        {
            this.time = time;
            this.density = density;
            this.speed = speed;
            this.tempareture = tempareture;
        }
    }
