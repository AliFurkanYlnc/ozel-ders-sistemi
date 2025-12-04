import React from 'react';
import { SafeAreaView, StyleSheet, Text } from 'react-native';

const StudentAvailabilityScreen: React.FC = () => {
  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.text}>Müsaitlik takvimini burada yöneteceksin.</Text>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f7f7f7',
  },
  text: {
    fontSize: 18,
    fontWeight: '600',
  },
});

export default StudentAvailabilityScreen;
