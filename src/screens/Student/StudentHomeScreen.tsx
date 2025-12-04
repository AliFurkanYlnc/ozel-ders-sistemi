import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

const StudentHomeScreen: React.FC = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Ana Sayfa</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 20,
    fontWeight: '700',
  },
});

export default StudentHomeScreen;
