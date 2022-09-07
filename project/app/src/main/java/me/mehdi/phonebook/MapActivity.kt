package me.mehdi.phonebook

import android.location.Location
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.AutoCompleteTextView
import me.mehdi.phonebook.databinding.ActivityMapBinding
import org.osmdroid.config.Configuration
import org.osmdroid.tileprovider.tilesource.TileSourceFactory
import org.osmdroid.util.GeoPoint
import org.osmdroid.views.MapView
import android.widget.ArrayAdapter
import android.view.View

class MapActivity : AppCompatActivity() {

    lateinit var mMap : MapView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val binding = ActivityMapBinding.inflate(layoutInflater)
        setContentView(binding.root)

        mMap = binding.mapView
        mMap.setTileSource(TileSourceFactory.MAPNIK)



        Configuration.getInstance().load(applicationContext, getSharedPreferences("phonebook_app", MODE_PRIVATE))

        val longitude = intent.getDoubleExtra("longitude", 8.5476)
        val latitude = intent.getDoubleExtra("latitude", 47.3764)


        val controller = mMap.controller

        val mapPoint = GeoPoint(latitude, longitude)

        controller.setZoom(19)

        controller.animateTo(mapPoint)

        val textView1 = findViewById<AutoCompleteTextView>(R.id.start)
        val suggestions1: Array<out String> = resources.getStringArray(R.array.suggestions)
        ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, suggestions1).also {
            adapter -> textView1.setAdapter(adapter)
        }
        val textView2 = findViewById<AutoCompleteTextView>(R.id.end)
        val suggestions2: Array<out String> = resources.getStringArray(R.array.suggestions)
        ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, suggestions2).also {
            adapter -> textView2.setAdapter(adapter)
        }

        fun searchRoute(view: View)   {
            //construct the route from A to B
            textView1.setText("Button Clicked")
        }
    }
}