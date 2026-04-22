import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Box, Typography, Grid, Card, CardContent, Button } from '@mui/material';
import { ShoppingCart } from '@mui/icons-material';
import { productAPI } from '../utils/api';

export default function HomePage() {

  const { data = [], isLoading } = useQuery({
    queryKey: ['products'],
    queryFn: async () => {
      const res = await productAPI.list({ limit: 8 });

      console.log("API RESPONSE:", res.data);

      // ✅ FIX (IMPORTANT)
      if (Array.isArray(res.data)) return res.data;
      if (Array.isArray(res.data?.products)) return res.data.products;

      return [];
    }
  });

  return (
    <Box>

      {/* HERO */}
      <Box sx={{
        p: 6,
        textAlign: 'center',
        background: 'linear-gradient(to right, #6366f1, #8b5cf6)',
        color: 'white'
      }}>
        <Typography variant="h3" fontWeight="bold">
          Welcome to ShopWave 🛒
        </Typography>

        <Typography mt={2}>
          Your one-stop shop for everything
        </Typography>
      </Box>

      {/* PRODUCTS */}
      <Box sx={{ p: 4 }}>
        <Typography variant="h5" mb={3}>
          Featured Products
        </Typography>

        {isLoading && <Typography>Loading...</Typography>}

        <Grid container spacing={3}>
          {data.map((p, i) => (
            <Grid item xs={12} sm={6} md={3} key={p.id || i}>
              <Card sx={{ textAlign: 'center', p: 2 }}>

                <Typography sx={{ fontSize: '3rem' }}>
                  {p.image_emoji || '📦'}
                </Typography>

                <CardContent>
                  <Typography fontWeight="bold">
                    {p.name}
                  </Typography>

                  <Typography color="green">
                    ₹{p.price}
                  </Typography>

                  <Button
                    variant="contained"
                    size="small"
                    startIcon={<ShoppingCart />}
                    sx={{ mt: 2 }}
                  >
                    Add to Cart
                  </Button>
                </CardContent>

              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

    </Box>
  );
}