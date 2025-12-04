import { NavigationContainer } from '@react-navigation/native';
import AuthStack from './AuthStack';
import StudentTabs from './StudentTabs';
import TutorTabs from './TutorTabs';
import useAuthStore from '../store/authStore';

const RootNavigator = () => {
  const { token, user } = useAuthStore();
  const isAuthenticated = Boolean(token && user);

  return (
    <NavigationContainer>
      {isAuthenticated ? (
        user?.role === 'student' ? <StudentTabs /> : <TutorTabs />
      ) : (
        <AuthStack />
      )}
    </NavigationContainer>
  );
};

export default RootNavigator;
