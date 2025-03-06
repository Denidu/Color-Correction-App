import 'package:flutter/material.dart';
import 'splash_screen.dart';

void main() {
  runApp(const ColorLoomApp());
}

class ColorLoomApp extends StatelessWidget {
  const ColorLoomApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        fontFamily: 'Serif',
      ),
      home: const SplashScreen(),
    );
  }
}