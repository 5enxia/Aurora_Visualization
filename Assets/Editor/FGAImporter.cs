using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using UnityEditor.Experimental.AssetImporters;

using System.IO;

[ScriptedImporter(1,"fga")]
public class FGAImporter : ScriptedImporter
{
    public override void OnImportAsset(AssetImportContext context)
    {
        var data = DeserializeVectorField(context.assetPath);
        if(data != null)
        {
            
        }
    }

    public static Texture3D DeserializeVectorField(string path)
    {
        //var stream = File.Open(path, FileMode.Open, FileAccess.Read, FileShare.Read);
        string text = File.ReadAllText(path);

        string[] AllFloats = text.Split(',');
        float Length = (float)AllFloats.Length - 10;
        int LengthPerSide = Mathf.RoundToInt(Mathf.Pow(Length / 3f, 1f / 3f));

        Texture3D VectorField = new Texture3D(LengthPerSide, LengthPerSide, LengthPerSide, TextureFormat.RGBAFloat, false);
        VectorField.wrapMode = TextureWrapMode.Repeat;

        float[] ConvertedFloats = new float[(int)Length];

        for (int i = 0; i < ConvertedFloats.Length - 1; i++)
        {
            ConvertedFloats[i] = float.Parse(AllFloats[i + 9]);
        }

        Color[] col = new Color[Mathf.RoundToInt(Length / 3f)];

        for (int i = 0; i < col.Length - 1; i++)
        {
            Vector3 v = Vector3.Normalize(new Vector3(ConvertedFloats[i * 3], ConvertedFloats[i * 3 + 1], ConvertedFloats[i * 3 + 2]));
            col[i] = new Color(v.x, v.y, v.z, 1f);
        }

        VectorField.SetPixels(col);
        VectorField.Apply(false);
        return VectorField;
    }
}


