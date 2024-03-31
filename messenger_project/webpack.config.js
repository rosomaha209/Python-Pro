const path = require('path');

module.exports = {
  entry: {  // Вхідні точки для ваших скриптів
    checkUserStatus: '/messenger/static/js/check_user_status.js',
    loginValidation: '/messenger/static/js/login_username_validation.js',
    registerValidation: '/messenger/static/js/register_username_validation.js'
  },
  output: {
    filename: '[name].bundle.js', // Назва вихідного файлу
    path: path.resolve(__dirname, 'messenger/static/dist'), // Шлях до папки з вихідними файлами
  },
  module: {
    rules: [
      {
        test: /\.css$/i,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          },
        },
      },
    ],
  },
};
