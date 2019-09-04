using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

using UnityEngine.Experimental.VFX;
using UnityEngine.Experimental.VFX.Utility;

using UnityEngine.EventSystems;

public class SolarWind_VFX : MonoBehaviour
{
    // Instance 
    public SolarWind sw;
    public string data_path = "Assets\\Data\\SolarWind\\";
    public string fn = "";

    public VisualEffect vfx;

    // Interaction for Debug
    public bool toggle_speed = false;
    public bool toggle_density = false;
    public bool toggle_temp = false;

    // Attribute 
    public ExposedParameter SPEED = "WindSpeed";
    public ExposedParameter DENSITY= "Density";
    public ExposedParameter TEMPARETURE = "Tempareture";

    // Start is called before the first frame update
    void Start()
    {
        // VFX
        vfx = GetComponent<VisualEffect>();

        // SolarWind
        sw = new SolarWind();
        fn = "SolarWind.json";
        sw = SolarWind.load(data_path + fn);
    }

    // Update is called once per frame
    void Update()
    {
        // Control Speed
        if (Input.GetKeyDown(KeyCode.Space)) {
            toggle_speed = !toggle_speed;
        }

        // Control Density (Num of Particle)
        if (Input.GetKeyDown(KeyCode.Return))
        {
            toggle_density = !toggle_density;
        }

        // Control Tempareture (Color)
        if (Input.GetKeyDown(KeyCode.T))
        {
            toggle_temp = !toggle_temp;
        }


        // Speed
        if (toggle_speed)
        {
            vfx.SetFloat(SPEED, sw.speed);
        }
        else
        {
            vfx.SetFloat(SPEED, 0);
        }

        // Density
        if (toggle_density)
        {
            vfx.SetFloat(DENSITY, sw.density);
        }
        else
        {
            vfx.SetFloat(SPEED, 0);
        }

        // Tempareture
        if (toggle_temp)
        {
            vfx.SetInt(TEMPARETURE, sw.tempareture);
        }
        else
        {
            vfx.SetInt(TEMPARETURE, 0);
        }
    }
}
