const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/index.js',  // Tệp đầu vào chính của bạn
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',  // Tên tệp đầu ra
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,  // Định nghĩa loại tệp cần biên dịch
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',  // Sử dụng babel-loader để biên dịch tệp .jsx
        },
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],  // Xử lý các tệp .js và .jsx
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',  // Tệp HTML mẫu
    }),
  ],
  devServer: {
    contentBase: path.join(__dirname, 'public'),
    compress: true,
    port: 9000,  // Chạy ứng dụng trên cổng 9000
  },
};
