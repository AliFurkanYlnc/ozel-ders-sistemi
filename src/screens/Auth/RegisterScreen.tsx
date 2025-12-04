import { SafeAreaView, StyleSheet, Text, View, Pressable } from 'react-native';

const RegisterScreen = () => {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.title}>Kayıt Ol</Text>
        <Text style={styles.subtitle}>Nasıl devam etmek istersin?</Text>
        <Pressable style={styles.button}>
          <Text style={styles.buttonText}>Öğrenciyim</Text>
        </Pressable>
        <Pressable style={styles.button}>
          <Text style={styles.buttonText}>Özel ders veriyorum</Text>
        </Pressable>
        <Text style={styles.placeholder}>Kayıt formu yakında burada olacak.</Text>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f2f2f2',
    justifyContent: 'center',
    paddingHorizontal: 24,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: '600',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    marginBottom: 16,
  },
  button: {
    backgroundColor: '#2d6cdf',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    width: '100%',
    alignItems: 'center',
    marginBottom: 12,
  },
  buttonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 16,
  },
  placeholder: {
    marginTop: 12,
    color: '#666',
    textAlign: 'center',
  },
});

export default RegisterScreen;
