import { SafeAreaView, StyleSheet, Text } from 'react-native';

const StudentHomeScreen = () => {
  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.text}>Öğrenci ana sayfasına hoş geldin!</Text>
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

export default StudentHomeScreen;
