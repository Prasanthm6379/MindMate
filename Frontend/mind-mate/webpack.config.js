// webpack.config.js
module.exports = {
    // Other Webpack configurations...
    module: {
      rules: [
        {
          test: /\.css$/,
          use: [
            'style-loader',
            'css-loader',
            {
              loader: 'postcss-loader',
              options: {
                postcssOptions: {
                  plugins: [
                    require('tailwindcss'), // Use tailwindcss directly
                    require('autoprefixer'),
                  ],
                },
              },
            },
          ],
        },
      ],
    },
  };