import 'package:flutter/material.dart';
import 'severity_level_screen.dart';

class ColorBlindnessTypeScreen extends StatelessWidget {
  const ColorBlindnessTypeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final colorBlindnessTypes = [
      {'title': 'Protanopia', 'description': 'Red-Blind · Severe condition'},
      {'title': 'Deuteranopia', 'description': 'Green-Blind · Severe condition'},
      {'title': 'Tritanopia', 'description': 'Blue-Blind · Severe condition'},
      {'title': 'Protanomaly', 'description': 'Red-Weak · Mild condition'},
      {'title': 'Deuteranomaly', 'description': 'Green-Weak · Most common condition'},
      {'title': 'Tritanomaly', 'description': 'Blue-Weak · Rare mild condition'},
    ];

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(120),
        child: AppBar(
          backgroundColor: Colors.white,
          elevation: 0,
          flexibleSpace: Padding(
            padding: const EdgeInsets.only(left: 16, top: 40, right: 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Image.asset(
                  'assets/colorloom.png',
                  width: 50,
                  height: 50,
                ),
                const SizedBox(height: 8),
                const Text(
                  'Select Your Color-Blindness Type',
                  style: TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                    fontFamily: 'Serif',
                    color: Colors.black,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: SingleChildScrollView(
          child: Column(
            children: List.generate(colorBlindnessTypes.length, (index) {
              return _buildTypeCard(
                context,
                colorBlindnessTypes[index]['title']!,
                colorBlindnessTypes[index]['description']!,
              );
            }),
          ),
        ),
      ),
    );
  }

  Widget _buildTypeCard(BuildContext context, String title, String description) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10.0),
      child: Card(
        elevation: 1,
        color: const Color(0xFFF5F5F5),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        child: ListTile(
          contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          title: Text(
            title,
            style: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              fontFamily: 'Serif',
            ),
          ),
          subtitle: Text(
            description,
            style: const TextStyle(
              color: Colors.grey,
              fontFamily: 'Serif',
            ),
          ),
          trailing: const Icon(Icons.arrow_forward, color: Colors.grey),
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => SeverityLevelScreen(selectedType: title),
              ),
            );
          },
        ),
      ),
    );
  }
}
